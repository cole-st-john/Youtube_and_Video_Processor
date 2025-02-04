"""Wrapper for ffmpeg tools"""

import os
import shutil
import subprocess
import sys

from rich import print


class Ffmpeg_Tools:
    """Composing and executing ffmpeg commands - enabling media processing"""

    # Resource: https://trac.ffmpeg.org/wiki/How%20to%20speed%20up%20/%20slow%20down%20a%20video

    ffmpeg_params: dict = dict()

    @classmethod
    def check_if_ffpmeg_available(cls):
        try:
            subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except FileNotFoundError:
            print(
                "Warning: FFMPEG is not installed or not available on the PATH.",
                "Please install it from https://ffmpeg.org/download.html",
                "& add to the PATH environmental variable.",
            )
            sys.exit()
        else:
            print("All dependencies found.")

    @classmethod
    def extract_cover_image(cls, video_path, cover_time, cover_image_path):
        """Cover image extraction based on time input"""
        ffmpeg_pic_args = [
            "ffmpeg",
            "-hide_banner",
            "-i",
            video_path,
            "-loglevel",
            "quiet",
            "-ss",
            cover_time,
            # "-vf",
            # "scale=320:320:force_original_aspect_ratio=decrease",
            "-vframes",
            "1",
            cover_image_path,
        ]
        cls.execute(ffmpeg_pic_args)

    @classmethod
    def process_video_only_changes(cls, video_path, output_path, start, end, speed):
        """Processing video changes - cutting, speed - to single video stream (likely with audio included)"""

        if any([start, end, speed]):
            # Cut =========================
            start = start or 0
            ffmpeg_args = [
                "ffmpeg",
                "-hide_banner",
                "-ss",
                start,
            ]

            ffmpeg_args += [
                "-loglevel",
                "quiet",
            ]

            if end:
                ffmpeg_args += [
                    "-to",
                    end,
                ]

            # Input of video =============
            ffmpeg_args += [
                "-i",
                video_path,
            ]

            if speed and speed >= 0.5 and speed <= 2:
                # -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]"
                ffmpeg_args += [
                    "-filter_complex",
                    f"[0:v]setpts={1 / speed}*PTS[v];[0:a]atempo={speed}[a]",
                ]

                # Mapping audio to video
                # TODO: DOES THIS WORK FOR VIDEO WITH NO AUDIO?
                ffmpeg_args += [
                    "-map",
                    "[v]",
                    "-map",
                    "[a]",
                ]

            # Avoid re-encoding if speed not changing - not sure what else drives this
            if not speed:
                ffmpeg_args += [
                    "-c",
                    "copy",
                ]

            # where to output it
            ffmpeg_args += [
                output_path,
                "-y",
            ]
            cls.execute(ffmpeg_args)
        else:
            # Or just copy to new naming?
            shutil.copy(video_path, output_path)
            # os.rename(video_path, output_path)

    @classmethod
    def process_audio_and_video(cls, video_path, audio_path, output_path, start, end, speed):
        """Combined and process: Cutting / re-encoding separate audio and video streams"""
        start = start or 0

        # For video cutting ======================
        ffmpeg_args = [
            "ffmpeg",
            "-hide_banner",
            "-ss",
            start,
        ]
        ffmpeg_args += [
            "-loglevel",
            "quiet",
        ]

        if end:
            ffmpeg_args += [
                "-to",
                end,
            ]

        # Audio + audio cutting ==================
        ffmpeg_args += [
            "-i",
            audio_path,
            "-ss",
            start,
        ]

        if end:
            ffmpeg_args += [
                "-to",
                end,
            ]

        # Mapping audio to video
        ffmpeg_args += [
            "-i",
            video_path,
        ]

        # Set actual new speed asked for by user
        # if speed and speed >= 0.5 and speed <= 2:
        #     ffmpeg_args += [
        #         "-filter:a",
        #         f"atempo={speed}",
        #     ]
        if speed and speed >= 0.5 and speed <= 2:
            # -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]"
            ffmpeg_args += [
                "-filter_complex",
                f"[1:v]setpts={1 / speed}*PTS[v];[0:a]atempo={speed}[a]",
            ]

            # Mapping audio to video
            ffmpeg_args += [
                "-map",
                "[v]",
                "-map",
                "[a]",
            ]

        else:
            # Mapping audio to video
            ffmpeg_args += [
                "-map",
                "0:a",
                "-map",
                "1",
            ]

        # Avoid re-encoding if speed not changing - not sure what else drives this
        if not speed:
            ffmpeg_args += [
                "-c",
                "copy",
            ]

        # Output path
        ffmpeg_args.append(output_path)

        # Run it
        cls.execute(ffmpeg_args)

    @classmethod
    def add_image_to_video(cls, vid_aud_path, cover, img_path, output_path):
        """Add cover photo to combined video"""

        if cover:
            # ffmpeg -i rad.mp4 -i lofer.jpg -map 1 -map 0 -c copy -disposition:0 attached_pic out.mp4
            ffmpeg_args = [
                "ffmpeg",
                "-hide_banner",
            ]

            ffmpeg_args += [
                "-i",
                vid_aud_path,
            ]
            ffmpeg_args += [
                "-loglevel",
                "quiet",
            ]

            ffmpeg_args += ["-i", img_path, "-map", "1", "-map", "0"]

            ffmpeg_args += [
                "-c",
                "copy",
            ]

            # cover related
            ffmpeg_args += [
                "-disposition:0",
                "attached_pic",
            ]

            ffmpeg_args += [
                output_path,
                "-y",
            ]

            cls.execute(ffmpeg_args)

        else:
            # Or just rename to new naming?
            os.rename(vid_aud_path, output_path)

    @classmethod
    def execute(cls, ffmpeg_args):
        """Process arguments in FFMPEG"""
        ffmpeg_args = [str(arg) for arg in ffmpeg_args]
        # print(" ".join(ffmpeg_args))
        subprocess.run(ffmpeg_args)
