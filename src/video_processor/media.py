import multiprocessing as mp
import os
import shutil
import subprocess
import sys
from tkinter import messagebox


from video_processor import ffmpeg_tools
from pytubefix import YouTube

# from pytubefix import exceptions as pytubeexceptions
from video_processor import video_job_gui
from video_processor.configuration import config

last_values_file_path = config.output_path
YT_LAST_VALUES_FILE_PATH = os.path.join(last_values_file_path, "last_values.json")


def inform_complete_and_query_open(video):
    """Let user know when a video job is complete"""
    msg_return_code = None
    if "windows" in config.platform:
        msg_return_code = messagebox.askyesno(
            title="Video Tool",
            message=f"Video work on {video} complete.\n\nOpen video product?",
        )

    return msg_return_code


class Image:
    """Object carrying common cover image information/methods"""

    def __init__(self, video_path, cover_time):
        self.path = config.output_path
        self.name = "cover_pic"
        self.ext = ".jpg"
        self.cover_image_path = self.generate_cover_img_path()
        self.generate_cover_image(video_path, cover_time)

    def generate_cover_img_path(self):
        suffix = "_" + str(os.getpid())
        temp_name_comp = self.name + suffix + self.ext
        return os.path.join(self.path, temp_name_comp)

    def generate_cover_image(self, video_path, cover_time):
        """Extracts thumbnail from video at certain time.
        ffmpeg syntax
        # ffmpeg -i "input.webm" -ss 00:00:01.000 -vframes 1  hallo.jpg
        """

        ffmpeg_tools.Ffmpeg_Tools.extract_cover_image(video_path, cover_time, self.cover_image_path)

        return self.cover_image_path


class Job:
    """Object enabling user input of  video job information and processing - including a stop flag for the app"""

    def __init__(self):
        # initialize
        self.raw_video_params: dict = dict()

        # processed video params
        self.stop_event = True
        self.url: str = ""
        self.filepath: str = ""
        self.name: str = ""
        self.start_time: float | None
        self.end_time: float | None
        self.cover_time: float | None
        self.speed_mult: float | None
        self.combined_stream = False
        self.valid_inputs = True

        # Process
        self.get_user_input_and_validate()

    def process_user_inputs(self, raw_job_params: dict):
        """Perform processing of raw gui-input parameters to correctly use or document them"""

        # Pushing into processed parameters
        self.url = raw_job_params.get("url", "")
        self.url = self.url.replace('"', "")
        self.url = self.url.split("&")[0] if "&" in self.url else self.url

        self.filepath = raw_job_params.get("filepath", "")
        self.name = raw_job_params.get("name", "")

        def time_conversion_to_secs(time_entry):
            # early return for no entry
            if not time_entry:
                return

            # account for two time formats
            if ":" in time_entry:
                split_items = time_entry.split(":")
                if len(split_items) == 2:
                    h, m, seconds = 0, *split_items
                else:
                    h, m, seconds = split_items
            else:
                h, m, seconds = 0, 0, time_entry
            h = h or 0
            m = m or 0
            seconds = seconds or 0

            # Ensure float
            h, m, seconds = float(h), float(m), float(seconds)

            # Turn to seconds for simplicity
            seconds = h * 3600 + m * 60 + seconds

            # print("time convert:", time_entry, seconds)
            return seconds

        self.start_time = time_conversion_to_secs(raw_job_params.get("start", 0)) or 0
        self.end_time = time_conversion_to_secs(raw_job_params.get("end", None))
        self.cover_time = time_conversion_to_secs(raw_job_params.get("cover", None))
        self.speed_mult = time_conversion_to_secs(raw_job_params.get("speed", None))

        # process filepath for quotations (windows)
        self.filepath = self.filepath.replace('"', "")

        if self.filepath:
            self.url = ""  # clear url and trust filepath as source
            self.combined_stream = True

    def retrieve_last_params_from_file(self):
        """At user request - pull in last used / saved parameters from local file"""
        raw_params = list()
        try:
            # Read previous file params from file
            with open(YT_LAST_VALUES_FILE_PATH) as file:
                raw_params = [str(line).strip() for line in file]

                def transform_nulls(x):
                    return None if x == "None" else x

                raw_params = [transform_nulls(x) for x in raw_params]

        except FileNotFoundError:
            return

        else:
            # Port in previous parameters
            self.raw_video_params["url"] = raw_params.pop(0)
            self.raw_video_params["filepath"] = raw_params.pop(0)
            self.raw_video_params["name"] = raw_params.pop(0)
            self.raw_video_params["start"] = raw_params.pop(0)
            self.raw_video_params["end"] = raw_params.pop(0)
            self.raw_video_params["cover"] = raw_params.pop(0)
            self.raw_video_params["speed"] = raw_params.pop(0)

    def validate_inputs(self):
        """Perform a few basic checks of the user inputs for video processing"""
        if self.url:
            try:
                YouTube(self.url, "WEB").check_availability()
            except Exception as ex:
                print(f"{ex}")
                self.valid_inputs = False
        if not any([self.filepath, self.url]):
            # TODO: ADD ERROR RAISING
            self.valid_inputs = False

        if not self.valid_inputs:
            print("Error - No valid URL or filepath given.")
            messagebox.showerror(
                title="Video Input Error",
                message="Invalid input for Video URL or Filepath.",
            )

    def get_user_input_and_validate(self):
        """Initiate GUI for user inputs and process/validate the raw inputs"""
        self.retrieve_last_params_from_file()
        self.stop_event, raw_video_params = video_job_gui.VideoJobGui(self).execute_gui()
        if self.stop_event:
            return
        self.process_user_inputs(raw_video_params)
        self.validate_inputs()


class Video_Processor:
    """Object owning video processing methods"""

    def __init__(self, job):
        self.video_process = str(os.getpid())
        self.processing_lock = mp.Lock()

        # initialize
        self.raw_video_params: dict = dict()

        # processed video params
        self.url: str = ""
        self.filepath: str = ""
        self.name: str = ""
        self.start_time: float | None
        self.end_time: float | None
        self.cover_time: float | None
        self.speed_mult: float | None
        self.combined_stream: bool

        # transfer properties?
        for key, value in job.__dict__.items():
            if key not in ("__name__",):
                setattr(self, key, value)

        # video processing related
        self.cover_image_path: str = ""
        self.video_stream: str | None = ""
        self.audio_stream: str | None = ""
        self.temp_raw_files = list()

        # Initiate Video Processing
        self.process_video()

    def process_video(self):
        # Ensure there is a path for final output
        self.final_path = self.generate_video_path()

        # Triage for whether yt download is required
        if self.url:
            self.download_from_yt()
        else:
            self.video_stream = self.filepath

        self.extract_cover_photo_from_video()
        self.perform_stream_composition()
        open_video_code = self.inform_of_process_completion()

        self.document_job_parameters()
        if open_video_code:
            self.open_video_result()
        self.clean_up_temp_files()

    def retrieve_last_params_from_file(self):
        """Pull previous video job parameters from a file - if there - to hand off to GUI"""
        raw_video_job_params = list()
        try:
            with open(YT_LAST_VALUES_FILE_PATH) as file:
                raw_video_job_params = [str(line.strip()) if not "None" else "" for line in file]
        except FileNotFoundError:
            return 0
        else:
            self.raw_video_params["url"] = raw_video_job_params.pop(0)
            self.raw_video_params["filepath"] = raw_video_job_params.pop(0)
            self.raw_video_params["name"] = raw_video_job_params.pop(0)
            self.raw_video_params["start"] = raw_video_job_params.pop(0)
            self.raw_video_params["end"] = raw_video_job_params.pop(0)
            self.raw_video_params["cover"] = raw_video_job_params.pop(0)
            self.raw_video_params["speed"] = raw_video_job_params.pop(0)

            return 1

    def document_job_parameters(self):
        """Document previous video job parameters to use in GUI next use - if desired by user."""

        # If the  new video was based on a local file - lets keep referring to the local file
        self.url = ""
        if self.filepath:
            pass
        else:
            self.filepath = self.final_path

        # Overwrite/create file contents with new parameters
        with open(YT_LAST_VALUES_FILE_PATH, "w") as file:
            value_string = "\n".join(
                [
                    str(x)
                    for x in [
                        self.url,
                        self.filepath,
                        self.name,
                        self.start_time,
                        self.end_time,
                        self.cover_time,
                        self.speed_mult,
                    ]
                ]
            )
            print(value_string)
            file.write(value_string)

    def generate_video_path(self):
        """Generates name and path - random name if no name & generates path"""
        # Generate a name if needed
        if not self.name:
            from random import randint

            self.name = "".join([str(randint(0, 9)) for _ in range(4)])

        # Assemble and return a full path
        return os.path.join(config.output_path, self.name + ".mp4")

    def download_from_yt(self):
        """If yt video,
        download it (it's stream(s)).
        Specifically - highest res stream:
        sometimes combined video / audio
        sometimes separate video / audio
        can have multiple file format output
        """

        # Early return if no youtube url to be downloaded
        if not self.url:
            return

        with self.processing_lock:
            yt_video_obj = YouTube(url=self.url, client="WEB")

            # get highest res video / and audio
            streams = yt_video_obj.streams

            # Get high res version
            stream = streams.filter(type="video").order_by("bitrate").desc().first()

            # Do we need to also look for separate audio stream
            combined_stream = stream.includes_audio_track

            # Generate a temp stream name
            temp_file_name = "temp_video" + "_" + self.video_process
            print(f"Downloading Video: {yt_video_obj.title}")

            # Download the stream
            self.video_stream = stream.download(config.output_path, filename=temp_file_name)

            # Inform complete
            print(f"Finished dl: {self.video_stream}")

            # Flag for later deletion / clean up
            self.temp_raw_files.append(self.video_stream)

            # Recording audio stream if there is separate audio stream as part of high res pairing
            if not combined_stream:
                # Generate temp stream name
                temp_file_name = "temp_audio" + "_" + self.video_process

                # Get available streams
                streams = yt_video_obj.streams

                # Download stream - highest res
                print("Downloading audio")
                self.audio_stream = (
                    streams.filter(type="audio")
                    .order_by("bitrate")
                    .desc()
                    .first()
                    .download(config.output_path, filename=temp_file_name)
                )
                print(f"Finished dl: {self.audio_stream}")

                # Flag for later completion
                self.temp_raw_files.append(self.audio_stream)

                # Ensure this flag is correct (edge case - no audio available and no audio included in vid)
                self.combined_stream = not self.audio_stream

    def extract_cover_photo_from_video(self):
        """Extract cover photo from video file"""
        if self.cover_time:
            with self.processing_lock:
                self.cover_image_path = Image(self.video_stream, self.cover_time).cover_image_path

                # Flag cover image for later deletion
                self.temp_raw_files.append(self.cover_image_path)

    def perform_stream_composition(self):
        with self.processing_lock:
            temp_combined_stream_path = os.path.join(
                config.output_path,
                self.name + "_" + self.video_process + "_combined.mp4",
            )
            ffmpeg_tools.Ffmpeg_Tools.process_video_only_changes(
                self.combined_stream,
                self.video_stream,
                temp_combined_stream_path,
                self.start_time,
                self.end_time,
                self.speed_mult,
            )

            ffmpeg_tools.Ffmpeg_Tools.process_audio_and_video(
                self.combined_stream,
                self.video_stream,
                self.audio_stream,
                temp_combined_stream_path,
                self.start_time,
                self.end_time,
                self.speed_mult,
            )

        self.apply_cover_photo(temp_combined_stream_path)

    def apply_cover_photo(self, temp_vid_aud_path):
        with self.processing_lock:
            ffmpeg_tools.Ffmpeg_Tools.add_image_to_video(
                temp_vid_aud_path,
                self.cover_time,
                self.cover_image_path,
                self.final_path,
            )

    def clean_up_temp_files(self):
        """delete temp files"""
        for a_file in self.temp_raw_files:
            try:
                os.remove(a_file)
            except Exception:
                pass

    def open_video_result(self):
        """open video file in default app - ie. vlc"""
        # TODO: DONT START UNTIL REENCODING COMPLETE
        with self.processing_lock:
            if "windows" in config.platform:
                os.startfile(self.final_path)
            if "wsl" in config.platform:
                try:
                    subprocess.run(
                        [
                            "wsl-open",
                            self.final_path,
                        ],
                        capture_output=True,
                    )
                except Exception:
                    print(f"Was not able to automatically open output file: {self.final_path}")

    def inform_of_process_completion(self):
        with self.processing_lock:
            print(f"Finished with job: {self.final_path}")
            return inform_complete_and_query_open(self.final_path)


def video_job_scheduler() -> bool:
    """
    Retrieves video job details and sends them for processing.

    Returns bool for whether User cancelled out of process.
    """

    # Check dependencies
    ffmpeg_tools.Ffmpeg_Tools.check_if_ffpmeg_available()

    # Get job details from user
    new_job = Job()

    # Return a flag that the user cancelled out
    if new_job.stop_event:
        return True

    # Otherwise put in a process queue
    if new_job.valid_inputs:
        job_to_process = mp.Process(target=Video_Processor, args=(new_job,))
        job_to_process.start()

    return False
