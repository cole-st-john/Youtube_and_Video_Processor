import tkinter as tk
import customtkinter
import sys
import os
import jsonpickle
from dataclasses import dataclass


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
        output_path = self.output_path_entry.get()

        # Compose values into config
        self.config_info = Configuration_Info(output_path)

        # Signal close
        self.destroy()

    def on_closing(self):
        # global stop_event
        self.user_quit = True
        print("User Chose to Exit Config Gui")
        sys.exit()

    def return_config_info(self):
        return self.config_info


@dataclass
class Configuration_Info:
    output_path: str


class Configuration:
    """Providing for user configuration of the app through gui and separate saving of configuration file"""

    def __init__(self):
        config_filename = "video_process_config.ini"
        self.config_path = os.path.dirname(os.path.abspath(__file__))
        self.config_fullpath = os.path.join(self.config_path, config_filename)
        self.config_info: Configuration_Info

    def prompt_user_for_config(self):
        self.config_info = Config_Gui().return_config_info()

    def validate_config(self):
        # Validate path =================================
        output_path = self.config_info.output_path
        output_path = output_path.replace('"', "")  # remove quotations
        if not os.path.isdir(output_path):
            self.prompt_user_for_config()
        self.config_info.output_path = output_path

    def store_config(self):
        # config -> json
        with open(self.config_fullpath, "w") as json_file:
            json_str = jsonpickle.encode(self.config_info)
            json_file.write(json_str)

    def get_config_information(self):
        # If no config - get values with gui and store them
        if not os.path.isfile(self.config_fullpath):
            print("Missing config file - creating it.")
            self.prompt_user_for_config()
            self.validate_config()
            self.store_config()

        # otherwise - pull in configuration details
        else:
            print("Found Config File - processing inputs.")
            # json -> config
            with open(self.config_fullpath) as json_file:
                json_str = json_file.read()
                self.config_info = jsonpickle.decode(
                    json_str, classes=Configuration_Info
                )

        return self.config_info


# Get configs
print("Executing configuration....")
config = Configuration().get_config_information()
