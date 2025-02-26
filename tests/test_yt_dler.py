import importlib.metadata
import os
import shutil
import sys
from pathlib import Path
import pytest
from rich import print

from video_processor import app, config, media  # , ffmpeg_tools, video_job_gui


@pytest.fixture(scope="session", autouse=True)
def check_dependencies():
    dependencies = ["pytest-env"]  # using env variable in pyproject.toml and pytest-env

    missing_dependencies = [pkg for pkg in dependencies if not importlib.metadata.version(pkg)]
    if missing_dependencies:
        pytest.skip(f"Skipping tests due to missing dependencies: {', '.join(missing_dependencies)}")


@pytest.fixture(scope="session")
def test_dir():
    path = Path(config.output_dir)

    # Ensure it's clean before running tests
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)

    yield path  # Provide the directory to tests

    # Cleanup after all tests finish
    shutil.rmtree(path, ignore_errors=True)


# Test resources
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
EXAMPLE_VIDEO_1 = "https://youtu.be/BsGjkkPKbsk"  # 6 seconds 720p
EXAMPLE_VIDEO_W_SHARE_AND_TIME = "https://youtu.be/KKYB59JZ4-4?si=kzLX0t0OhktE0CX_&t=1"  # 5 second video
EXAMPLE_VIDEO_W_SHARE = "https://youtu.be/KKYB59JZ4-4?si=kzLX0t0OhktE0CX_"
SHORT_VIDEO_1 = "https://www.youtube.com/shorts/zthRM9pI6TQ"  # < 5 seconds
VIDEO_IN_PLAYLIST_1 = "https://www.youtube.com/watch?v=KKYB59JZ4-4&list=PLrU3Bc28AUqz7NCQfpzRuALldz8uAx9Ns"
PLAYLIST = "https://www.youtube.com/playlist?list=PLrU3Bc28AUqz7NCQfpzRuALldz8uAx9Ns"
INVALID_VIDEO = "https://www.youtube.com/shorts/AFDFSSSDFF4GG444"
LOW_QUALITY_VIDEO = "https://www.youtube.com/watch?v=V6R-nEiTwcs"  # 480p
ULTRA_HD_VIDEO = "https://www.youtube.com/watch?v=R3GfuzLMPkA"  # 2160p
LOCAL_VIDEO_VALID = os.path.join(TEST_DIR, "test_resources", "video_1.mp4")
LOCAL_VIDEO_VALID_WITH_QUOTES = '"' + LOCAL_VIDEO_VALID + '"'
LOCAL_VIDEO_INVALID = os.path.join(TEST_DIR, "test_resources", "video_not_existing.mp4")


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
        new_job.url = SHORT_VIDEO_1
        new_job.name = f"{sys._getframe().f_code.co_name}"
        new_job.stop_event = False
        media.Video_Processor(new_job).process_job_async()
        assert 1 == 1

    def test_job_processing_2(self, test_dir):
        new_job = media.Job()
        new_job.url = SHORT_VIDEO_1
        new_job.name = f"{sys._getframe().f_code.co_name}"
        new_job.start_time = 1
        new_job.end_time = 2
        new_job.cover_time = 0
        new_job.speed_mult = 0.5
        new_job.stop_event = False
        success_flag, path = media.Video_Processor(new_job).process_job_sync()
        assert success_flag is True and os.path.isfile(path)

    def test_job_processing_4(self, test_dir):
        new_job = media.Job()
        new_job.url = EXAMPLE_VIDEO_1
        new_job.name = f"{sys._getframe().f_code.co_name}"
        new_job.start_time = 1
        new_job.end_time = 2
        success_flag, path = media.Video_Processor(new_job).process_job_sync()
        assert success_flag is True and os.path.isfile(path)

    def test_job_processing_5(self, test_dir):
        new_job = media.Job()
        new_job.url = EXAMPLE_VIDEO_W_SHARE_AND_TIME
        new_job.name = f"{sys._getframe().f_code.co_name}"
        new_job.start_time = 1
        new_job.end_time = 2
        success_flag, path = media.Video_Processor(new_job).process_job_sync()
        assert success_flag is True and os.path.isfile(path)

    def test_job_processing_6(self, test_dir):
        new_job = media.Job()
        new_job.url = EXAMPLE_VIDEO_W_SHARE
        new_job.name = f"{sys._getframe().f_code.co_name}"
        new_job.start_time = 1
        new_job.end_time = 2
        success_flag, path = media.Video_Processor(new_job).process_job_sync()
        assert success_flag is True and os.path.isfile(path)

    def test_job_processing_7(self, test_dir):
        new_job = media.Job()
        new_job.url = VIDEO_IN_PLAYLIST_1
        new_job.name = f"{sys._getframe().f_code.co_name}"
        new_job.start_time = 1
        new_job.end_time = 2
        success_flag, path = media.Video_Processor(new_job).process_job_sync()
        assert success_flag is True and os.path.isfile(path)

    def test_job_processing_8(self, test_dir):
        with pytest.raises(media.YoutubeURLError):
            new_job = media.Job()
            new_job.url = INVALID_VIDEO
            media.Video_Processor(new_job).process_job_sync()

    def test_job_processing_9(self, test_dir):
        new_job = media.Job()
        new_job.url = LOW_QUALITY_VIDEO
        new_job.name = f"{sys._getframe().f_code.co_name}"
        new_job.start_time = 1
        new_job.end_time = 2
        success_flag, path = media.Video_Processor(new_job).process_job_sync()
        assert success_flag is True and os.path.isfile(path)

    def test_job_processing_10(self, test_dir):
        new_job = media.Job()
        new_job.url = ULTRA_HD_VIDEO
        new_job.name = f"{sys._getframe().f_code.co_name}"
        new_job.start_time = 1
        new_job.end_time = 2
        success_flag, path = media.Video_Processor(new_job).process_job_sync()
        assert success_flag is True and os.path.isfile(path)

    def test_job_processing_11(self, test_dir):
        with pytest.raises(media.YoutubeURLError):
            new_job = media.Job()
            new_job.url = PLAYLIST
            media.Video_Processor(new_job).process_job_sync()

    def test_job_processing_12(self, test_dir):
        with pytest.raises(media.InvalidInputs):
            new_job = media.Job()
            new_job.url = ""
            media.Video_Processor(new_job).process_job_sync()

    def test_job_processing_13(self, test_dir):
        new_job = media.Job()
        new_job.filepath = LOCAL_VIDEO_VALID
        new_job.start_time = 1
        new_job.end_time = 3
        new_job.name = f"{sys._getframe().f_code.co_name}"
        success_flag, path = media.Video_Processor(new_job).process_job_sync()
        assert success_flag is True and os.path.isfile(path)

    def test_job_processing_14(self, test_dir):
        with pytest.raises(FileNotFoundError):
            new_job = media.Job()
            new_job.filepath = LOCAL_VIDEO_INVALID
            media.Video_Processor(new_job).process_job_sync()
