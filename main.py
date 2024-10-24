"""This package / project enables manual input of youtube download jobs -
the download and processing of the video/audio happens asynchronously."""

import media
import multiprocessing as mp


def dependency_check():
    media.ffmpeg_command.check_if_available()
    print("All dependencies found.")


def video_downloader_and_processor() -> None:
    """Start video downloader and processor app"""
    # Constants / Flags
    continue_flag = True

    # Event Flag for signaling process termination in subprocesses
    stop_event = mp.Event()

    # Check whether there is a returned "done" flag, if not, continue
    while continue_flag:
        # create new video job (using gui) - block on the gui - but then allow async processing
        continue_flag = not media.video_job_scheduler()

        # Check if the event is set (meaning a process signaled to stop)
        if not continue_flag:
            print("Ending Video app elegantly.")


if __name__ == "__main__":
    dependency_check()
    video_downloader_and_processor()
