import pytest
import sys
import os
from configuration import config
import media

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import main


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

EXAMPLE_VIDEO_1 = "https://youtu.be/BsGjkkPKbsk"


class Test_Integration:
    def test_does_it_work_for_simple_case_1(self):
        main.video_downloader_and_processor()
        assert 1 == 1


class Test_File:
    """Testing"""

    def test_file_object_basics_1(self):
        """
        Given: File object
        When: given no basename or path
        Then: returns default graphml basename and working dir path
        """
        pass

    #     test_file_obj = File()
    #     assert isinstance(test_file_obj, File)
    #     assert test_file_obj.basename == "temp.graphml"
    #     assert test_file_obj.window_search_name == "temp.graphml - yEd"
    #     assert test_file_obj.dir.lower() == os.getcwd().lower()


# def check_whether_inputs_valid(url, filepath):


def test_show_completed_msg():
    """
    Given: nothing - base unit test
    When: calling message box
    Then: msg shows up
    """
    video_name = "ABC.mp4"
    media.show_completed_msg(video_name)
    assert 1 == 1  # assert made it this far


# class ffmpeg_command:
#     def extract_cover_image(cls, video_path, cover_time, cover_image_path):
#     def process_video_only_changes(
#         cls, single_stream, video_path, output_path, start, end, speed
#     ):
#     def process_audio_and_video(
#         cls, single_stream, video_path, audio_path, output_path, start, end, speed
#     ):
#     def add_image_to_video(cls, vid_aud_path, cover, img_path, output_path):
#     def execute(cls, ffmpeg_pic_args):


# class Image:
#     def __init__(self, video_path, cover_time):
#     def generate_cover_img_path(self):
#     def generate_cover_image(self, video_path, cover_time):


class Test_Job:

    def test_init(self):
        pass 

    def begin_process(self):
    def process_inputs(self, raw_params: dict):
    def retrieve_last_params_from_file(self):
    def get_user_input_and_validate(self):


# class Video:
#     def begin_process(self):
#     def retrieve_last_params_from_file(self):
#     def document_job(self):
#     def generate_video_path(self):
#     def download_from_yt(self):
#     def extract_cover_photo(self):
#     def perform_composition(self):
#     def apply_cover_photo(self, temp_vid_aud_path):
#     def clean_up(self):
#     def open(self):
#     def inform_complete(self):


# def instantiate_video(job):
# def process_video(job):
# def video_job_scheduler():


    """
    Given: gui input data, including valid file path
    When: processing video
    Then: should process from filepath
    """

    """
    Given: gui input data, including valid youtube url with high res streams
    When: processing video
    Then: should create video with vid/aud from url
    """

    """
    Given: gui input data, including valid youtube url with only low-res combined mp4
    When: processing video
    Then: should skip audio/video comb stream 
    """

    """
    Given: gui input data, with times in seconds
    When: processing video
    Then: should use time in seconds
    """

    """
    Given: gui input data, with times in mm:ss(.s*)?
    When: processing video
    Then: should use time in converted seconds
    """
    