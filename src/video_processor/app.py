"""
This package / project enables
- download of youtube videos,
- simple modification of output length through clipping,
- allows adding a cover image from somewhere in the video,
- modification of video speed,
and all through manual input in a desktop GUI -
including asynchronous download and processing of the video/audio streams.
"""

from video_processor import media
from video_processor.configuration import config  # get config info / early warning

APP_NAME = "Video downloader and processor app"


def video_downloader_and_processor(end_flag=False) -> None:
    """Execute video downloader and processor app"""

    print(f"Starting {APP_NAME}", "=" * 10)

    # Check if the end flag is set (meaning user signaled to stop further videos)
    while not end_flag:
        # create new video job (using gui) - block on the gui - but then allow async processing
        end_flag = media.video_job_scheduler()

    print(f"Closing {APP_NAME}.", "=" * 10)


# if __name__ == "__main__":
#     # Enter app loop
#     print("Calling directly")
#     video_downloader_and_processor()
# else:
#     print("Calling indirectly")
#     video_downloader_and_processor()
