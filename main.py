"""
This package / project enables
- download of youtube videos,
- simple modification of output length through clipping,
- allows adding a cover image from somewhere in the video,
- modification of video speed,
and all through manual input in a desktop GUI -
including asynchronous download and processing of the video/audio streams.
"""

# import pdb; pdb.set_trace()
import media

from configuration import config  # get config info / early warning
import ffmpeg_tools

# import os

# envi = os.environ
# print(envi)
# patho = os.path


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
    ffmpeg_tools.Ffmpeg_Tools.check_if_ffpmeg_available()

    # Start app
    video_downloader_and_processor()

    print("Finished")
