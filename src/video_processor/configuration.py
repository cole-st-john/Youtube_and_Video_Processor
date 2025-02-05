"""Provides general configuration information and guis for the application"""

import os
import subprocess
import sys
import tkinter as tk
from dataclasses import dataclass
from platform import platform

import customtkinter
import jsonpickle
from rich import print


class Config_Gui(customtkinter.CTk):
    """Providing a GUI for configuration process"""

    def __init__(self):
        super().__init__()
        # self.geometry(f"{1100}x{580}")

        # GUI SETTINGS ====================================
        self.inputs_frame_dict = {
            "row": 0,
            "column": 0,
            "columnspan": 2,
            "rowspan": 5,
            "padx": (20, 20),
            "pady": (20, 20),
            "sticky": "nsew",
        }

        self.output_path_label_dict = {
            "row": 0,
            "column": 0,
            # "columnspan": 12,
            "padx": (20, 20),
            "pady": (20, 20),
            "sticky": "nsew",
        }

        self.output_path_entry_dict = {
            "row": 0,
            "column": 1,
            # "columnspan": 12,
            "padx": (20, 20),
            "pady": (20, 20),
            "sticky": "nsew",
        }

        self.entry_confirm_btn_dict = {
            "row": 7,
            "column": 1,
            "columnspan": 2,
            "padx": (20, 20),
            "pady": (20, 20),
            "sticky": "nsew",
        }

        # configure window ===============
        self.title("Video Processing - Config")
        self.grid_columnconfigure((0, 1), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Frame
        self.inputs_frame = customtkinter.CTkFrame(self)
        self.inputs_frame.grid(**self.inputs_frame_dict)

        # output path

        self.output_path_label = tk.Label(self.inputs_frame, text="Output Path: ")
        self.output_path_label.grid(**self.output_path_label_dict)

        self.output_path_textvar = tk.StringVar()
        self.output_path_entry = customtkinter.CTkEntry(
            self.inputs_frame,
            placeholder_text="Enter filepath here",
            textvariable=self.output_path_textvar,
        )
        self.output_path_entry.grid(**self.output_path_entry_dict)

        # Confirm Button
        self.entry_confirm_btn = customtkinter.CTkButton(
            master=self.inputs_frame,
            text="Confirm",
            # fg_color="green2",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.gather_input,
        )
        self.entry_confirm_btn.grid(**self.entry_confirm_btn_dict)

        # Start GUI!
        self.enter_gui_exec()

    def enter_gui_exec(self):
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainloop()

    def gather_input(self):
        # Query values
        self.output_dir = self.output_path_entry.get().replace('"', "")

        # Signal close
        self.destroy()

    def on_closing(self):
        # global stop_event
        self.user_quit = True
        print("User chose to exit configuration gui.")
        sys.exit()

    def transfer_config(self, other):
        Stored_Config(self.output_dir).load(other)


def check_app_dependencies():
    """Check app dependencies"""

    def check_if_ffpmeg_available():
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

    check_if_ffpmeg_available()


@dataclass
class Stored_Config:
    output_dir: str

    def valid(self) -> bool:
        """validate stored config items (before use)"""
        valid_check = True
        if not os.path.isdir(self.output_dir):
            valid_check = False
        return valid_check

    def load(self, other) -> None:
        """load stored configs into Config object"""
        if self.valid():
            for key, value in self.__dict__.items():
                if key and key not in ("__name__",):
                    setattr(other, key, value)


@dataclass
class Config:
    """Providing for user configuration of the app through gui and separate saving of configuration file"""

    output_dir: str = ""
    config_dir: str = os.getcwd()
    run_interactive: bool = os.getenv("TEST_MODE") != "1"
    APP_NAME: str = "Video Downloader And Processor App"
    GUI_APPEARANCE_MODE: str = "System"
    GUI_COLOR_THEME: str = "blue"
    CONFIG_FILENAME: str = "video_process_config.json"
    LAST_VALUES_FILENAME: str = "last_values.json"
    platform: str = platform().lower()
    config_path: str = os.path.join(config_dir, CONFIG_FILENAME)
    existing_config: bool = os.path.isfile(config_path)
    last_values_filepath: str = ""

    VALID_GUI_COLOR_THEMES = {"blue", "green", "dark-blue"}
    VALID_GUI_APPEARANCES = {"System", "Dark", "Light"}

    def load_saved(self):
        with open(self.config_path) as json_file:
            json_str = json_file.read()
            saved_config: Stored_Config = jsonpickle.decode(json_str, classes=Stored_Config)  # type: ignore
            if saved_config:
                saved_config.load(self)

    def prompt_user_for_config(self):
        Config_Gui().transfer_config(self)

    def store_config(self):
        # config -> json
        with open(self.config_path, "w") as json_file:
            json_str = jsonpickle.encode(Stored_Config(self.output_dir))
            json_file.write(str(json_str))

    def set_dependent_config_elements(self):
        self.last_values_filepath = os.path.join(self.output_dir, self.LAST_VALUES_FILENAME)

    def valid_config(self):
        """Validate config"""
        if not self.output_dir:
            return False
        if not os.path.isdir(self.output_dir):
            return False
        # if self.GUI_APPEARANCE_MODE not in self.VALID_GUI_APPEARANCES:
        #     return False
        # if not os.path.isdir(self.config_dir):
        #     return False
        return True

    def set(self):
        print(f"Configuring {self.APP_NAME}")

        check_app_dependencies()

        if self.run_interactive:
            if self.existing_config:
                self.load_saved()

            while not self.valid_config():
                self.prompt_user_for_config()

            self.store_config()

        else:
            # make temporary directory in cwd for outputs of tests
            self.output_dir = os.path.join(self.config_dir, "tests", "test_temp")

            # we wont store the test config

        self.set_dependent_config_elements()

        return self


config = Config().set()
