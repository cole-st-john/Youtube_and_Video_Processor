import os
import sys
import importlib.metadata
import pytest

# import inspect
# import video_processor
from video_processor import app, media  # , ffmpeg_tools, video_job_gui

# Checking test dependencies
dependencies = ["pytest-env"]


def check_dependencies(dependencies):
    def pkg_installed(package_name):
        try:
            importlib.metadata.version(package_name)
            return True
        except importlib.metadata.PackageNotFoundError:
            return False

    missing_dependencies = [pkg for pkg in dependencies if not pkg_installed(pkg)]
    if any(missing_dependencies):
        raise ImportError(f"Missing some package dependencies: {'\n'.join(missing_dependencies)}")


# using env variable in pyproject.toml and pytest-env
check_dependencies(dependencies)


# different tests resources
TEST_DIR = os.path.dirname(os.path.abspath(__file__))

EXAMPLE_VIDEO_1 = "https://youtu.be/BsGjkkPKbsk"
SHORT_VIDEO_1 = "https://www.youtube.com/shorts/zthRM9pI6TQ"
SHORT_VIDEO_2 = "https://www.youtube.com/shorts/o5Q7GShNo3Q"
VIDEO_IN_PLAYLIST_1 = "https://www.youtube.com/shorts/o5Q7GShNo3Q"
PLAYLIST = "https://www.youtube.com/shorts/o5Q7GShNo3Q"
INVALID_VIDEO = "https://www.youtube.com/shorts/o5Q7GShNo3Q"
LOW_QUALITY_VIDEO = "https://www.youtube.com/shorts/o5Q7GShNo3Q"
ULTRA_HD_VIDEO = "https://www.youtube.com/shorts/o5Q7GShNo3Q"
LOCAL_VIDEO_VALID = os.path.join(TEST_DIR, "test_resources", "video_1.mp4")
LOCAL_VIDEO_INVALID = os.path.join(TEST_DIR, "test_resources", "video_not_existing.mp4")


# testing gui
# testing dl functionality
# testing composition functionality
# testing

# edge cases

"""
Given: File object
When: given no basename or path
Then: returns default graphml basename and working dir path
"""


# Integration Tests =====================================
# main ====================
class Test_Integration:
    def test_does_it_work_for_simple_case_1(self):
        app.video_downloader_and_processor()
        assert 1 == 1


# Unit Tests ============================================
# configuration ====================
class Test_Config_Gui:
    pass


# Job processing
class Test_Job_Processing:
    def test_job_processing_1(self):
        new_job = media.Job()
        new_job.url = "https://www.youtube.com/shorts/zthRM9pI6TQ"
        # new_job.name = "async1"
        new_job.name = f"{sys._getframe().f_code.co_name}"
        new_job.stop_event = False
        media.process_job_async(new_job)
        assert 1 == 1

    def test_job_processing_2(self):
        new_job = media.Job()
        new_job.url = "https://www.youtube.com/shorts/zthRM9pI6TQ"
        new_job.name = f"{sys._getframe().f_code.co_name}"
        new_job.stop_event = False
        success_flag = media.process_job_sync(new_job)
        assert success_flag is True

    def test_job_processing_3(self):
        new_job = media.Job()
        new_job.url = "https://www.youtube.com/shorts/zthRM9pI6TQ"
        new_job.name = f"{sys._getframe().f_code.co_name}"
        new_job.start_time = 1
        new_job.end_time = 2
        new_job.cover_time = 0
        new_job.speed_mult = 0.5
        success_flag = media.process_job_sync(new_job)
        assert success_flag is True
