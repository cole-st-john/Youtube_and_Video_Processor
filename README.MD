# Just another Youtube and Video Processor

I find myself commonly wanting to quickly process or archive youtube or other local videos for personal use in knowledge archival.   This project incorporates the functions that I most appreciated, and with a decent gui interface so that it can support the project as a standalone EXE with no visible terminal / terminal feedback.


## Current functionality

This is just another app around quickly fulfilling the needs I have most frequently experienced:

- Downloading high quality youtube videos (audio and video streams) or specifying local video file 
- If separate streams - recombining media streams.
- Cutting video / audio to single contiguous section - time from / time to
- Changing video / audio speed together
- Adding a specific cover image based on a time / frame in the video


## Installing Dependencies

### Get Python Dependencies:

Using pip:

``
pip install -r requirements.txt
``

Or **Better**, using UV (Kudos to Astral and Team) - 

``
pip install uv 
uv sync
``

### Getting External Core Components

- Download FFMPEG (.EXE)  from https://ffmpeg.org/download.html

- Add that directory to PATH environment variable.


# Example Usage: 

Downloading video from youtube: 

´´
python main.py
´´


Enter video details:

![Entering details in gui](https://raw.githubusercontent.com/cole-st-john/youtube_and_video_processor/master/images/example1.gif)

Enjoy processed video