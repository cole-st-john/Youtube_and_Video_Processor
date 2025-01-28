import os
import sys

from video_processor import app

# import unittest
import pytest

# Work-around as non-installed package
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


# different tests resources
EXAMPLE_VIDEO_1 = "https://youtu.be/BsGjkkPKbsk"
SHORT_VIDEO = "https://www.youtube.com/shorts/zthRM9pI6TQ"
LONG_VIDEO = "https://www.youtube.com/shorts/o5Q7GShNo3Q"
VIDEO_IN_PLAYLIST = "https://www.youtube.com/shorts/o5Q7GShNo3Q"
PLAYLIST = "https://www.youtube.com/shorts/o5Q7GShNo3Q"
INVALID_VIDEO = "https://www.youtube.com/shorts/o5Q7GShNo3Q"
LOW_QUALITY_VIDEO = "https://www.youtube.com/shorts/o5Q7GShNo3Q"
ULTRA_HD_VIDEO = "https://www.youtube.com/shorts/o5Q7GShNo3Q"
LOCAL_VIDEO_VALID = os.path.join(SCRIPT_DIR, "test_resources", "video_1.mp4")
LOCAL_VIDEO_INVALID = os.path.join(SCRIPT_DIR, "test_resources", "video_not_existing.mp4")


# unittest.TestCase
# def setUp(self):

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
