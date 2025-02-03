import multiprocessing as mp
import os

# import shutil
import subprocess

# import sys
import tkinter as tk
from tkinter import messagebox as msg
from random import randint
from pytubefix import YouTube

# from pytubefix import exceptions as pytubeexceptions
from video_processor.ffmpeg_tools import Ffmpeg_Tools
from video_processor import video_job_gui
from video_processor.configuration import config


class YoutubeURLError(Exception):
    pass


def open_video_dialog(video_name):
    """If running app interactively, ask user whether the video product should be opened -> returns bool."""
    msg_box_yes_no = None

    # some root tk window
    root = tk.Tk()
    root.withdraw()
    print("See message_box to open video ===========")
    if root._windowingsystem == "win32":
        # windows showerror
        top = tk.Toplevel(root)
        top.iconify()
        msg_box_yes_no = msg.askyesno(title="Video Tool", message=f"Video work on {video_name} complete.\n\nOpen video product?", parent=top)
        top.destroy()
    else:
        # non-windows showerror
        msg_box_yes_no = msg.askyesno(
            title="Video Tool",
            message=f"Video work on {video_name} complete.\n\nOpen video product?",
        )

    root.destroy()

    return msg_box_yes_no


def sync_wrapper(func):
    """impose synchronous lock during the wrapped 'work'"""

    def sync_arg_wrapper(self, *args, **kwargs):
        with self.processing_lock:
            return func(self, *args, **kwargs)

    return sync_arg_wrapper


# def yt_parse_url(url):
#     # https://www.youtube.com/watch?v=RVmq1tFerRc
#     # https://www.youtube.com/watch?v=KKYB59JZ4-4
#     # https://youtu.be/KKYB59JZ4-4?si=jXTKdXyiVA32v5yy
#     # https://youtu.be/KKYB59JZ4-4

#     # playlist
#     # https://www.youtube.com/watch?v=5XDld3npn0o&list=PLov10-5x6sFFk3pBv6EMudwIZJXaEpGXf

#     # time
#     # https://youtu.be/5XDld3npn0o?si=JUyC5K59_0_uyliL&t=14

#     # short or long
#     #   tps://youtube.com/shorts/IzLD1t4SrUE?si=1hpk-YE5gDz1jjm4 (share ending)

#     pass


def yt_is_valid_url(url):
    if not url:
        return False
    try:
        YouTube(url, "WEB").check_availability()
        return True
    except Exception:
        return False


def yt_get_streams(url):
    """return all stream for a youtube url"""
    return YouTube(url=url, client="WEB").streams


def yt_filter_video_streams(streams):
    return streams.filter(type="video")


def yt_filter_highest_quality_video_stream(video_streams):
    return video_streams.order_by("bitrate").desc().first()


def yt_video_stream_includes_audio(video_stream):
    return video_stream.includes_audio_track


# def yt_audio_available(streams):
#     return bool(yt_filter_highest_quality_audio_streams(streams))


def yt_filter_highest_quality_audio_stream(streams):
    return streams.filter(type="audio").order_by("bitrate").desc().first()


def gen_name(name=None):
    """Generates random digit set"""
    if not name:
        name = "".join([str(randint(0, 9)) for _ in range(6)])
    return name


def yt_gen_name_suffix(media_type):
    if media_type == "video":
        return "temp_video"
    else:  # type==Video or None
        return "temp_audio"


def yt_gen_temp_name(name, type=None):
    type = type or "video"  # enum: audio, video
    return name + "_" + yt_gen_name_suffix(type) + ".mp4"


def yt_download_stream(stream, path, name):
    print(f"Downloading {stream.title}:{name}")
    return stream.download(path, filename=name)


# def yt_filter_highest_quality_audio_stream(audio_streams):
#     return audio_streams.order_by("bitrate").desc().first()


class Image:
    """Object carrying common cover image information/methods"""

    def __init__(self, video_path, cover_time):
        self.path = config.config_info.output_path
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

        Ffmpeg_Tools.extract_cover_image(video_path, cover_time, self.cover_image_path)

        return self.cover_image_path


class Job:
    """Object enabling user input of  video job information and processing - including a stop flag for the app"""

    def __init__(self):
        # initialize
        self.raw_video_params: dict = dict()

        # processed video params
        self.stop_event = False

        # string entries
        self.url: str = ""
        self.filepath: str = ""
        self.name: str = ""

        # float entries
        self.start_time: float | None = None
        self.end_time: float | None = None
        self.cover_time: float | None = None
        self.speed_mult: float | None = None

        self.combined_stream = False
        self.valid_inputs = True
        self.processed_output_path: str = ""

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
            with open(config.LAST_VALUES_FULLPATH) as file:
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
            msg.showerror(
                title="Video Input Error",
                message="Invalid input for Video URL or Filepath.",
            )

    def get_input(self):
        """Initiate GUI for user inputs and process/validate the raw inputs"""
        self.retrieve_last_params_from_file()
        self.stop_event, raw_video_params = video_job_gui.VideoJobGui(self).execute_gui()
        if self.stop_event:
            return self
        self.process_user_inputs(raw_video_params)
        self.validate_inputs()

        return self  # return the processed Job instance

    def document_job_parameters(self):
        """Document previous video job parameters to use in GUI next use - if desired by user."""

        # If the  new video was based on a local file - lets keep referring to the local file
        self.url = ""
        if self.filepath:
            pass
        else:
            self.filepath = self.processed_output_path

        # Overwrite/create file contents with new parameters
        with open(config.LAST_VALUES_FULLPATH, "w") as file:
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
            # print(value_string)
            file.write(value_string)


class Video_Processor:
    """Object owning video processing methods"""

    def __init__(self, job):
        # initialize
        # self.raw_video_params: dict = dict()
        self.job = job

        # Enablers of async job processing
        self.video_process = str(os.getpid())
        self.processing_lock = mp.Lock()

        # processed video params
        # self.url: str = ""
        # self.filepath: str = ""
        # self.name: str = ""
        # self.start_time: float | None
        # self.end_time: float | None
        # self.cover_time: float | None
        # self.speed_mult: float | None

        # video processing related
        self.is_youtube_job = bool(job.url)
        self.combined_stream: bool
        self.includes_video: bool
        self.includes_audio: bool
        self.multiple_streams: bool
        self.cover_image_path: str = ""
        self.local_video_stream: str | None = ""
        self.local_audio_stream: str | None = ""
        self.temp_raw_files = list()

        # modifying job
        self.output_dir = config.config_info.output_path
        self.job.name = gen_name(job.name)
        self.temp_combined_stream_path = os.path.join(
            self.output_dir,
            self.job.name + "_combined.mp4",
        )
        self.job.processed_output_path = self.generate_video_path()

    def job_runnable(self):
        return bool(self.job.valid_inputs)

    def return_success_flag(self):
        # TODO: ADD FFMPEG CHECK FOR USABLE MEDIA?
        if os.path.isfile(self.job.processed_output_path):
            return True
        else:
            return False

    def process_video_only(self):
        Ffmpeg_Tools.process_video_only_changes(
            self.local_video_stream,
            self.temp_combined_stream_path,
            self.job.start_time,
            self.job.end_time,
            self.job.speed_mult,
        )

    def combine_and_process_streams(self):
        Ffmpeg_Tools.process_audio_and_video(
            self.local_video_stream,
            self.local_audio_stream,
            self.temp_combined_stream_path,
            self.job.start_time,
            self.job.end_time,
            self.job.speed_mult,
        )

    def process_yt_job(self):
        self.download_from_yt()
        self.extract_cover_photo_from_video()
        if self.local_audio_stream and self.local_video_stream:
            self.combine_and_process_streams()
        else:
            self.process_video_only()

    def process_local_job(self):
        self.local_video_stream = self.job.filepath  # FIXME: HACK FOR PATHINIG
        self.extract_cover_photo_from_video()
        self.process_video_only()

    def wrap_up_job(self):
        self.job.document_job_parameters()

        if config.RUN_INTERACTIVE and open_video_dialog(self.job.processed_output_path):
            self.open_video_result()

        self.clean_up_temp_files()

    def process_job(self):
        # Triage for whether yt download is required

        if self.is_youtube_job:
            self.process_yt_job()
        else:
            self.process_local_job()

        self.apply_cover_photo(self.temp_combined_stream_path)

        # self.perform_stream_composition()

        self.wrap_up_job()

        return self.return_success_flag(), self.job.processed_output_path

    def process_job_async(self) -> None:
        """Async processing of video processing jobs"""
        if self.job_runnable:
            job_to_process = mp.Process(target=self.process_job)
            job_to_process.start()

    def process_job_sync(self) -> bool:
        """Async processing of video processing jobs"""
        if self.job_runnable:
            success_flag, _ = self.process_job()
            return success_flag
        return False

    def generate_video_path(self):
        """Generates path - random name if no name & generates path"""

        # Assemble and return a full path
        return os.path.join(self.output_dir, self.job.name + ".mp4")

    @sync_wrapper
    def download_from_yt(self):
        """If yt video,
        download it (it's stream(s)).
        Specifically - highest res stream:
        sometimes combined video / audio
        sometimes separate video / audio
        can have multiple file format output
        """

        # Check that its actually available
        if not yt_is_valid_url(self.job.url):
            raise YoutubeURLError(f"URL seems to be bad / unavailable {self.job.url}")

        # Fetch youtube streams
        streams = yt_get_streams(self.job.url)

        # Select and download video
        yt_video_stream = yt_filter_highest_quality_video_stream(streams)
        # print(f"Downloading Video: {yt_video_stream.title}")
        self.local_video_stream = yt_download_stream(yt_video_stream, self.output_dir, yt_gen_temp_name(self.job.name, type="video"))
        self.temp_raw_files.append(self.local_video_stream)

        # if audio only available seperately in high quality - select and download audio
        if not yt_video_stream_includes_audio(yt_video_stream):
            yt_audio_stream = yt_filter_highest_quality_audio_stream(streams)
            self.local_audio_stream = yt_download_stream(yt_audio_stream, self.output_dir, yt_gen_temp_name(self.job.name, type="audio"))
            self.temp_raw_files.append(self.local_audio_stream)

    @sync_wrapper
    def extract_cover_photo_from_video(self):
        """Extract cover photo from video file"""
        if self.job.cover_time:
            self.cover_image_path = Image(self.local_video_stream, self.job.cover_time).cover_image_path

            # Flag cover image for later deletion
            self.temp_raw_files.append(self.cover_image_path)

    def apply_cover_photo(self, temp_vid_aud_path):
        Ffmpeg_Tools.add_image_to_video(
            temp_vid_aud_path,
            self.job.cover_time,
            self.cover_image_path,
            self.job.processed_output_path,
        )

    def clean_up_temp_files(self):
        """delete temp files"""
        for a_file in self.temp_raw_files:
            try:
                os.remove(a_file)
            except Exception:
                pass

    @sync_wrapper
    def open_video_result(self):
        """open video file in default app - ie. vlc"""
        # TODO: DONT START UNTIL REENCODING COMPLETE

        if "windows" in config.config_info.platform:
            os.startfile(self.job.processed_output_path)
        if "wsl" in config.config_info.platform:
            try:
                subprocess.run(
                    [
                        "wsl-open",
                        self.job.processed_output_path,
                    ],
                    capture_output=True,
                )
            except Exception:
                print(f"Was not able to automatically open output file: {self.job.processed_output_path}")


def video_downloader_and_processor(end_flag=False):
    """Execute video downloader and processor app"""

    print(f"Starting {config.APP_NAME}", "=" * 10)

    # Check if the end flag is set (meaning user signaled to stop further videos)
    while not end_flag:
        # create new video job (using gui) - block on the gui - but then allow async processing

        # Instantiate new job and get user input
        new_job = Job().get_input()

        # update end_flag
        end_flag = new_job.stop_event

        if end_flag:
            break

        # Process Job
        try:
            Video_Processor(new_job).process_job_async()
            # Video_Processor(new_job).process_job_sync()  # for debugging
        except Exception as e:
            print(f"Error in dl of {new_job} - error: {e}")
            # pass  # FIXME:

    print(f"Closing {config.APP_NAME}.", "=" * 10)

    # TODO: IS THERE IS A PROBLEM IF AN ASYNC PROCESS IS WORKING WHEN IT GETS HERE ?
