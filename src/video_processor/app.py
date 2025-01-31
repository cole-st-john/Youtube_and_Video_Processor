"""
This package / project enables
- download of youtube videos,
- simple modification of output length through clipping,
- allows adding a cover image from somewhere in the video,
- modification of video speed,
and all through manual input in a desktop GUI -
including asynchronous download and processing of the video/audio streams.
"""

from video_processor.media import video_downloader_and_processor

if __name__ == "__main__":
    video_downloader_and_processor()
