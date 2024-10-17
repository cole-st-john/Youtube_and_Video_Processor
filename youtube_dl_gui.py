import tkinter as tk
import customtkinter
import os
import sys

customtkinter.set_appearance_mode(
    "System"
)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


last_values_file_path = os.getcwd()
YT_LAST_VALUES_FILE_PATH = os.path.join(last_values_file_path, "last_values.json")


class VideoGui(customtkinter.CTk):
    """
    App
    """

    def __init__(self, video_params):
        super().__init__()
        # self.geometry(f"{1100}x{580}")

        self.raw_gui_video_params = video_params

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

        self.url_label_dict = {
            "row": 0,
            "column": 0,
            # "columnspan": 12,
            "padx": (20, 20),
            "pady": (20, 20),
            "sticky": "nsew",
        }

        self.url_entry_dict = {
            "row": 0,
            "column": 1,
            # "columnspan": 12,
            "padx": (20, 20),
            "pady": (20, 20),
            "sticky": "nsew",
        }

        self.filepath_label_dict = {
            "row": 1,
            "column": 0,
            # "columnspan": 12,
            "padx": (20, 20),
            "pady": (20, 20),
            "sticky": "nsew",
        }

        self.file_entry_dict = {
            "row": 1,
            "column": 1,
            "columnspan": 12,
            "padx": (20, 20),
            "pady": (20, 20),
            "sticky": "nsew",
        }

        self.name_label_dict = {
            "row": 2,
            "column": 0,
            # "columnspan": 12,
            "padx": (20, 20),
            "pady": (20, 20),
            "sticky": "nsew",
        }

        self.name_entry_dict = {
            "row": 2,
            "column": 1,
            "columnspan": 12,
            "padx": (20, 20),
            "pady": (20, 20),
            "sticky": "nsew",
        }

        self.start_label_dict = {
            "row": 3,
            "column": 0,
            # "columnspan": 12,
            "padx": (20, 20),
            "pady": (20, 20),
            "sticky": "nsew",
        }

        self.start_entry_dict = {
            "row": 3,
            "column": 1,
            # "columnspan": 12,
            "padx": (20, 20),
            "pady": (20, 20),
            "sticky": "nsew",
        }

        self.end_label_dict = {
            "row": 4,
            "column": 0,
            # "columnspan": 12,
            "padx": (20, 20),
            "pady": (20, 20),
            "sticky": "nsew",
        }

        self.end_entry_dict = {
            "row": 4,
            "column": 1,
            # "columnspan": 12,
            "padx": (20, 20),
            "pady": (20, 20),
            "sticky": "nsew",
        }

        self.cover_label_dict = {
            "row": 5,
            "column": 0,
            # "columnspan": 12,
            "padx": (20, 20),
            "pady": (20, 20),
            "sticky": "nsew",
        }

        self.cover_entry_dict = {
            "row": 5,
            "column": 1,
            # "columnspan": 12,
            "padx": (20, 20),
            "pady": (20, 20),
            "sticky": "nsew",
        }

        self.speed_label_dict = {
            "row": 6,
            "column": 0,
            # "columnspan": 12,
            "padx": (20, 20),
            "pady": (20, 20),
            "sticky": "nsew",
        }

        self.speed_entry_dict = {
            "row": 6,
            "column": 1,
            # "columnspan": 12,
            "padx": (20, 20),
            "pady": (20, 20),
            "sticky": "nsew",
        }

        self.last_values_btn_dict = {
            "row": 7,
            "column": 0,
            "columnspan": 2,
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
        self.title("Video DL and Cutting Tool")
        self.grid_columnconfigure((0, 1), weight=0)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.create_set_shortcuts_elements()

    # Main GUI Elements ==========================================
    def create_set_shortcuts_elements(self):
        # overall frame ===========================
        self.inputs_frame = customtkinter.CTkFrame(self)
        self.inputs_frame.grid(**self.inputs_frame_dict)

        # url

        self.url_label = tk.Label(self.inputs_frame, text="Youtube URL:")
        self.url_label.grid(**self.url_label_dict)

        self.url_textvar = tk.StringVar()
        self.url_entry = customtkinter.CTkEntry(
            self.inputs_frame,
            placeholder_text="Youtube URL",
            textvariable=self.url_textvar,
        )
        self.url_entry.grid(**self.url_entry_dict)

        # File
        self.filepath_label = tk.Label(self.inputs_frame, text="Filepath:")
        self.filepath_label.grid(**self.filepath_label_dict)

        self.file_textvar = tk.StringVar()
        self.file_entry = customtkinter.CTkEntry(
            self.inputs_frame,
            placeholder_text="Video Filepath",
            textvariable=self.file_textvar,
        )
        self.file_entry.grid(**self.file_entry_dict)

        # Name
        self.name_label = tk.Label(self.inputs_frame, text="Name:")
        self.name_label.grid(**self.name_label_dict)

        self.name_textvar = tk.StringVar()
        self.name_entry = customtkinter.CTkEntry(
            self.inputs_frame,
            placeholder_text="Name",
            textvariable=self.name_textvar,
        )
        self.name_entry.grid(**self.name_entry_dict)

        # Start Time
        self.start_label = tk.Label(self.inputs_frame, text="Start Time:")
        self.start_label.grid(**self.start_label_dict)
        self.start_var = tk.StringVar()
        self.start_entry = customtkinter.CTkEntry(
            self.inputs_frame,
            placeholder_text="Start Time",
            textvariable=self.start_var,
        )
        self.start_entry.grid(**self.start_entry_dict)

        # End Time
        self.end_label = tk.Label(self.inputs_frame, text="End Time:")
        self.end_label.grid(**self.end_label_dict)
        self.end_var = tk.StringVar()
        self.end_entry = customtkinter.CTkEntry(
            self.inputs_frame,
            placeholder_text="End Time",
            textvariable=self.end_var,
        )
        self.end_entry.grid(**self.end_entry_dict)

        # Cover photo time
        self.cover_label = tk.Label(self.inputs_frame, text="Cover Photo Time:")
        self.cover_label.grid(**self.cover_label_dict)
        self.cover_var = tk.StringVar()
        self.cover_entry = customtkinter.CTkEntry(
            self.inputs_frame,
            placeholder_text="Cover Photo Time",
            textvariable=self.cover_var,
        )
        self.cover_entry.grid(**self.cover_entry_dict)

        # Speed
        self.speed_label = tk.Label(self.inputs_frame, text="Speed")
        self.speed_label.grid(**self.speed_label_dict)
        self.speed_var = tk.StringVar()
        self.speed_entry = customtkinter.CTkEntry(
            self.inputs_frame,
            placeholder_text="1x (no x needed)",
            textvariable=self.speed_var,
        )
        self.speed_entry.grid(**self.speed_entry_dict)

        # last values button
        self.last_values_btn = customtkinter.CTkButton(
            master=self.inputs_frame,
            text="Populate Last Values",
            # fg_color="green2",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.enter_last_values,
        )
        self.last_values_btn.grid(**self.last_values_btn_dict)

        # Confirm Button
        self.entry_confirm_btn = customtkinter.CTkButton(
            master=self.inputs_frame,
            text="Confirm",
            # fg_color="green2",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.confirm_entries,
        )
        self.entry_confirm_btn.grid(**self.entry_confirm_btn_dict)

    def time_conversion(self, entry):
        if ":" in entry:
            split_items = entry.split(":")
            if len(split_items) == 2:
                h, m, seconds = 0, *split_items
            else:
                h, m, seconds = split_items
        else:
            h, m, seconds = 0, 0, entry
        h = h or 0
        m = m or 0
        seconds = seconds or 0

        h, m, seconds = float(h), float(m), float(seconds)

        seconds = h * 3600 + m * 60 + seconds
        print("time convert:", entry, seconds)
        return str(seconds)

    def enter_last_values(self):
        # check for file
        # get last values
        if not any(self.raw_gui_video_params):
            print("No last values found")
            return

        url = self.raw_gui_video_params["url"]
        filepath = self.raw_gui_video_params["filepath"]
        name = self.raw_gui_video_params["name"]
        start = self.raw_gui_video_params["start"]
        end = self.raw_gui_video_params["end"]
        cover = self.raw_gui_video_params["cover"]
        speed = self.raw_gui_video_params["speed"]

        # populate last values
        self.url_textvar.set(url)
        self.file_textvar.set(filepath)
        self.name_textvar.set(name)
        if float(start):
            self.start_var.set(start)
        if float(end):
            self.end_var.set(end)
        if float(cover):
            self.cover_var.set(cover)
        if float(speed):
            self.speed_var.set(speed)

        # refresh gui
        self.update()

    def confirm_entries(self):
        self.raw_gui_video_params["url"] = self.url_entry.get()
        self.raw_gui_video_params["filepath"] = self.file_entry.get()
        self.raw_gui_video_params["name"] = self.name_entry.get()
        self.raw_gui_video_params["start"] = self.start_entry.get()
        self.raw_gui_video_params["end"] = self.end_entry.get()
        self.raw_gui_video_params["cover"] = self.cover_entry.get()
        self.raw_gui_video_params["speed"] = self.speed_entry.get()

        self.destroy()

    def on_closing(self):
        global stop_event
        stop_event.set()
        print("Exiting")
        self.destroy()
        # sys.exit()

    def get_user_input(self):
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainloop()
        return self.raw_gui_video_params
