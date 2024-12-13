import os
import sys

import main
import media

import unittest
import pytest


# unittest.TestCase
# def setUp(self):

# different tests


EXAMPLE_VIDEO_1 = "https://youtu.be/BsGjkkPKbsk"
EXAMPLE_VIDEO_2 = "https://www.youtube.com/shorts/zthRM9pI6TQ"
EXAMPLE_VIDEO_3 = "https://www.youtube.com/shorts/o5Q7GShNo3Q"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


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
        main.video_downloader_and_processor()
        assert 1 == 1


# Unit Tests ============================================
# configuration ====================
class Test_Config_Gui:
    pass
