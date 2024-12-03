"""This package / project enables manual input of youtube download jobs -
the download and processing of the video/audio happens asynchronously."""

import media
from configuration import config  # get config info / early warning


def video_downloader_and_processor() -> None:
    """Start video downloader and processor app"""

    # Check whether there is a returned "end" flag, if not, continue
    end_flag = False

    while not end_flag:
        # create new video job (using gui) - block on the gui - but then allow async processing
        end_flag = media.video_job_scheduler()

        # Check if the end flag is set (meaning user signaled to stop further videos)
        if end_flag:
            print("Ending Video app elegantly.")


if __name__ == "__main__":
    # Check dependencies
    media.Ffmpeg_Command.check_if_available()

    # Start app
    video_downloader_and_processor()

    print("Finished")
