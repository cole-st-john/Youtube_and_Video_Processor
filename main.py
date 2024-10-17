"""This package / project enables manual input of youtube download jobs -
the download and processing of the video/audio happens asynchronously."""

from . import media
import multiprocessing as mp


def video_downloader_and_processor() -> None:
    """Start video downloader and processor app"""
    # Constants / Flags
    continue_flag = True

    # Event Flag for signaling process termination in subprocesses
    stop_event = mp.Event()

    # Check whether there is a returned "done" flag, if not, continue
    while continue_flag:
        # create new video job (using gui) - block on the gui - but then allow async processing
        media.video_job_scheduler()

        # Check if the event is set (meaning a process signaled to stop)
        if stop_event.is_set():
            print("Ending Video app.")
            continue_flag = False  # Exit the while loop


if __name__ == "__main__":
    video_downloader_and_processor()
