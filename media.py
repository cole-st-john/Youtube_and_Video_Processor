from tkinter import messagebox
import subprocess
import os
from pytubefix import YouTube
from pytubefix import exceptions as pytubeexceptions
import video_job_gui
import multiprocessing as mp
import sys
from configuration import config
import shutil


last_values_file_path = config.output_path
YT_LAST_VALUES_FILE_PATH = os.path.join(last_values_file_path, "last_values.json")


def show_completed_msg(video):
    """Let user know when a video job is complete"""
    messagebox.showinfo(title="Video Tool", message=f"Video work on {video} complete.")


class ffmpeg_command:
    """Composing and executing ffmpeg commands - enabling media processing"""

    # Resource: https://trac.ffmpeg.org/wiki/How%20to%20speed%20up%20/%20slow%20down%20a%20video

    ffmpeg_params: dict = dict()

    @classmethod
    def check_if_available(cls):
        try:
            subprocess.run(
                ["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except FileNotFoundError:
            print(
                "Warning: FFMPEG is not installed or not available on the PATH.",
                "Please install it from https://ffmpeg.org/download.html",
                "& add to the PATH environmental variable.",
            )
            sys.exit()
        else:
            print("All dependencies found.")

    @classmethod
    def extract_cover_image(cls, video_path, cover_time, cover_image_path):
        """Cover image extraction based on time input"""
        ffmpeg_pic_args = [
            "ffmpeg",
            "-i",
            video_path,
            "-ss",
            cover_time,
            # "-vf",
            # "scale=320:320:force_original_aspect_ratio=decrease",
            "-vframes",
            "1",
            cover_image_path,
        ]
        cls.execute(ffmpeg_pic_args)

    @classmethod
    def process_video_only_changes(
        cls, single_stream, video_path, output_path, start, end, speed
    ):
        """Processing video changes - cutting, speed"""
        if single_stream:
            if any([start, end, speed]):
                # Cut =========================
                ffmpeg_args = [
                    "ffmpeg",
                    "-ss",
                    start,
                ]

                if end:
                    ffmpeg_args += [
                        "-to",
                        end,
                    ]

                # Input of video =============
                ffmpeg_args += [
                    "-i",
                    video_path,
                ]

                if speed and speed >= 0.5 and speed <= 2:
                    # -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]"
                    ffmpeg_args += [
                        "-filter_complex",
                        f"[0:v]setpts={1/speed}*PTS[v];[0:a]atempo={speed}[a]",
                    ]

                    # Mapping audio to video
                    ffmpeg_args += [
                        "-map",
                        "[v]",
                        "-map",
                        "[a]",
                    ]

                # Avoid re-encoding if speed not changing - not sure what else drives this
                if not speed:
                    ffmpeg_args += [
                        "-c",
                        "copy",
                    ]

                # where to output it
                ffmpeg_args += [
                    output_path,
                    "-y",
                ]
                cls.execute(ffmpeg_args)
            else:
                # Or just copy to new naming?
                shutil.copy(video_path, output_path)
                # os.rename(video_path, output_path)

    @classmethod
    def process_audio_and_video(
        cls, single_stream, video_path, audio_path, output_path, start, end, speed
    ):
        """Cutting / re-encoding audio and video streams"""
        if not single_stream:
            # For video cutting ======================
            ffmpeg_args = [
                "ffmpeg",
                "-ss",
                start,
            ]

            if end:
                ffmpeg_args += [
                    "-to",
                    end,
                ]

            # Audio + audio cutting ==================
            ffmpeg_args += [
                "-i",
                audio_path,
                "-ss",
                start,
            ]

            if end:
                ffmpeg_args += [
                    "-to",
                    end,
                ]

            # Mapping audio to video
            ffmpeg_args += [
                "-i",
                video_path,
            ]

            # Set actual new speed asked for by user
            # if speed and speed >= 0.5 and speed <= 2:
            #     ffmpeg_args += [
            #         "-filter:a",
            #         f"atempo={speed}",
            #     ]
            if speed and speed >= 0.5 and speed <= 2:
                # -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]"
                ffmpeg_args += [
                    "-filter_complex",
                    f"[1:v]setpts={1/speed}*PTS[v];[0:a]atempo={speed}[a]",
                ]

                # Mapping audio to video
                ffmpeg_args += [
                    "-map",
                    "[v]",
                    "-map",
                    "[a]",
                ]

            else:
                # Mapping audio to video
                ffmpeg_args += [
                    "-map",
                    "0:a",
                    "-map",
                    "1",
                ]

            # Avoid re-encoding if speed not changing - not sure what else drives this
            if not speed:
                ffmpeg_args += [
                    "-c",
                    "copy",
                ]

            # Output path
            ffmpeg_args.append(output_path)

            # Run it
            cls.execute(ffmpeg_args)

    @classmethod
    def add_image_to_video(cls, vid_aud_path, cover, img_path, output_path):
        """Add cover photo to combined video"""

        if cover:
            # ffmpeg -i rad.mp4 -i lofer.jpg -map 1 -map 0 -c copy -disposition:0 attached_pic out.mp4
            ffmpeg_args = [
                "ffmpeg",
            ]

            ffmpeg_args += [
                "-i",
                vid_aud_path,
            ]

            ffmpeg_args += ["-i", img_path, "-map", "1", "-map", "0"]

            ffmpeg_args += [
                "-c",
                "copy",
            ]

            # cover related
            ffmpeg_args += [
                "-disposition:0",
                "attached_pic",
            ]

            ffmpeg_args += [
                output_path,
                "-y",
            ]

            cls.execute(ffmpeg_args)

        else:
            # Or just rename to new naming?
            os.rename(vid_aud_path, output_path)

    @classmethod
    def execute(cls, ffmpeg_args):
        ffmpeg_args = [str(arg) for arg in ffmpeg_args]
        print(" ".join(ffmpeg_args))
        subprocess.run(ffmpeg_args)


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
        # ffmpeg -i "Dont suck  SUCK CREEK RACE.webm" -ss 00:00:01.000 -vframes 1  hallo.jpg
        """

        ffmpeg_command.extract_cover_image(
            video_path, cover_time, self.cover_image_path
        )

        return self.cover_image_path


class Job:
    """Object enabling async job information and processing - including the stop flag"""

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
        self.single_stream = False
        self.valid_inputs = True

        # Process
        self.begin_process()

    def begin_process(self):
        self.get_user_input_and_validate()

    def process_inputs(self, raw_params: dict):
        """Perform processing of raw gui-input parameters to correctly use or document them"""

        # Pushing into processed parameters
        self.url = raw_params.get("url", "")
        self.url = self.url.replace('"', "")
        self.url = self.url.split("&")[0] if "&" in self.url else self.url

        self.filepath = raw_params.get("filepath", "")
        self.name = raw_params.get("name", "")

        def float_convert(param):
            if param:
                return float(param)

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

        self.start_time = time_conversion_to_secs(raw_params.get("start", 0)) or 0
        self.end_time = time_conversion_to_secs(raw_params.get("end", None))
        self.cover_time = time_conversion_to_secs(raw_params.get("cover", None))
        self.speed_mult = time_conversion_to_secs(raw_params.get("speed", None))

        # process filepath for quotations (windows)
        self.filepath = self.filepath.replace('"', "")

        if self.filepath:
            self.url = ""
            self.single_stream = True

        # Validate Url
        if self.url:
            # if just id - make work for that

            # valid url check
            # priority - url
            # self.filepath = ""
            pass

    def retrieve_last_params_from_file(self):
        """At user request - pull in last used / saved parameters from local file"""
        raw_params = list()
        try:
            with open(YT_LAST_VALUES_FILE_PATH) as file:
                raw_params = [str(line).strip() for line in file]

                def transform_nulls(x):
                    return None if x == "None" else x

                raw_params = [transform_nulls(x) for x in raw_params]
        except FileNotFoundError:
            return
            # return 0
        else:
            self.raw_video_params["url"] = raw_params.pop(0)
            self.raw_video_params["filepath"] = raw_params.pop(0)
            self.raw_video_params["name"] = raw_params.pop(0)
            self.raw_video_params["start"] = raw_params.pop(0)
            self.raw_video_params["end"] = raw_params.pop(0)
            self.raw_video_params["cover"] = raw_params.pop(0)
            self.raw_video_params["speed"] = raw_params.pop(0)

            # return 1

    def validate_inputs(self):
        if not any([self.filepath, self.url]):
            # TODO: ADD ERROR RAISING
            self.valid_inputs = False
            print("Error - No valid URL or filepath given.")
            messagebox.showerror(
                title="Video Inputs - Error",
                message="Invalid input for Video URL or Filepath.",
            )

    def get_user_input_and_validate(self):
        """Initiate GUI for user inputs and process/validate the raw inputs"""
        self.retrieve_last_params_from_file()
        self.stop_event, raw_video_params = video_job_gui.VideoGui(
            self
        ).get_user_input()
        if self.stop_event:
            return
        self.process_inputs(raw_video_params)
        self.validate_inputs()


class Video:
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
        self.single_stream: bool

        # transfer properties?
        for key, value in job.__dict__.items():
            if key not in ("__name__",):
                setattr(self, key, value)

        # video processing related
        self.cover_image_path: str = ""
        self.video_stream: str | None = ""
        self.audio_stream: str | None = ""
        self.temp_raw_files = list()

        # Process
        self.begin_process()

    def begin_process(self):
        # self.get_user_input()
        self.final_path = self.generate_video_path()
        # Triage
        if self.url:
            self.download_from_yt()
        else:
            self.video_stream = self.filepath
        self.extract_cover_photo()
        self.perform_composition()
        self.inform_complete()
        self.document_job()
        self.open()
        self.clean_up()

    def retrieve_last_params_from_file(self):
        raw_params = list()
        try:
            with open(YT_LAST_VALUES_FILE_PATH) as file:
                raw_params = [str(line.strip()) if not "None" else "" for line in file]
        except FileNotFoundError:
            return 0
        else:
            self.raw_video_params["url"] = raw_params.pop(0)
            self.raw_video_params["filepath"] = raw_params.pop(0)
            self.raw_video_params["name"] = raw_params.pop(0)
            self.raw_video_params["start"] = raw_params.pop(0)
            self.raw_video_params["end"] = raw_params.pop(0)
            self.raw_video_params["cover"] = raw_params.pop(0)
            self.raw_video_params["speed"] = raw_params.pop(0)

            return 1

    def document_job(self):
        self.filepath = self.final_path
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
        """gives name if no name & generates path"""
        if not self.name:
            from random import randint

            self.name = "".join([str(randint(0, 9)) for _ in range(4)])
        return os.path.join(config.output_path, self.name + ".mp4")

    def download_from_yt(self):
        """If yt video, downloads highest res stream:
        sometimes combined video / audio
        sometimes separate video / audio
        can have multiple file formats
        """

        # Early return
        if not self.url:
            return

        with self.processing_lock:
            try:
                yt_video_obj = YouTube(url=self.url)

                # get highest res video / and audio
                streams = yt_video_obj.streams
                stream = streams.filter(type="video").order_by("bitrate").desc().first()
                if stream:
                    single_stream = stream.includes_audio_track
                else:
                    # TODO:

                    return

                # Downloading video stream in high res
                temp_file_name = "temp_video" + "_" + self.video_process
                print(f"Downloading Video: {yt_video_obj.title}")

                self.video_stream = stream.download(
                    config.output_path, filename=temp_file_name
                )
            except pytubeexceptions.VideoUnavailable as ex:
                print(f"This is not a valid video:\n{self.url}")
                return

            print(f"Finished dl: {self.video_stream}")
            self.temp_raw_files.append(self.video_stream)

            # Recording audio stream if there is separate audio stream as part of high res pairing
            if not single_stream:
                streams = yt_video_obj.streams
                temp_file_name = "temp_audio" + "_" + self.video_process
                print("Downloading audio")
                self.audio_stream = (
                    streams.filter(type="audio")
                    .order_by("bitrate")
                    .desc()
                    .first()
                    .download(config.output_path, filename=temp_file_name)
                )
                print(f"Finished dl: {self.audio_stream }")
                self.temp_raw_files.append(self.audio_stream)

                self.single_stream = not self.audio_stream

    def extract_cover_photo(self):
        """Extract cover photo"""
        if self.cover_time:
            with self.processing_lock:
                self.cover_image_path = Image(
                    self.video_stream, self.cover_time
                ).cover_image_path
                self.temp_raw_files.append(self.cover_image_path)

    def perform_composition(self):
        with self.processing_lock:
            temp_vid_aud_path = os.path.join(
                config.output_path,
                self.name + "_" + self.video_process + "_proc_aud_vid.mp4",
            )
            ffmpeg_command.process_video_only_changes(
                self.single_stream,
                self.video_stream,
                temp_vid_aud_path,
                self.start_time,
                self.end_time,
                self.speed_mult,
            )

            ffmpeg_command.process_audio_and_video(
                self.single_stream,
                self.video_stream,
                self.audio_stream,
                temp_vid_aud_path,
                self.start_time,
                self.end_time,
                self.speed_mult,
            )

        self.apply_cover_photo(temp_vid_aud_path)

    def apply_cover_photo(self, temp_vid_aud_path):
        with self.processing_lock:
            ffmpeg_command.add_image_to_video(
                temp_vid_aud_path,
                self.cover_time,
                self.cover_image_path,
                self.final_path,
            )

    def clean_up(self):
        # delete temp files
        for a_file in self.temp_raw_files:
            try:
                os.remove(a_file)
            except Exception:
                pass

    def open(self):
        """open video file in default app - ie. vlc"""
        # TODO: DONT START UNTIL REENCODING COMPLETE
        with self.processing_lock:
            os.startfile(self.final_path)

    def inform_complete(self):
        print(f"Finished with job: {self.final_path}")
        show_completed_msg(self.final_path)


def instantiate_video(job):
    return Video(job)


def process_video(job):
    return Video(job)


def video_job_scheduler() -> bool:
    """Retrieves video job details and sends them for processing"""

    new_job = Job()

    if new_job.stop_event:
        return True

    if new_job.valid_inputs:
        job_to_process = mp.Process(target=process_video, args=(new_job,))
        job_to_process.start()

    return False
