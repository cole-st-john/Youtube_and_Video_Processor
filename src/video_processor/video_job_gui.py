from tkinter import StringVar

import customtkinter

from video_processor.configuration import config

customtkinter.set_appearance_mode(config.GUI_APPEARANCE_MODE)
customtkinter.set_default_color_theme(config.GUI_COLOR_THEME)


class VideoJobGui(customtkinter.CTk):
    """
    App for user entry of video job parameters
    """

    def __init__(self, job):
        super().__init__()
        self.user_quit = False
        self.job = job
        self.raw_gui_video_params = self.job.raw_video_params

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
            # "columnspan": 2,
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

        # Bind function for upon closing app with x
        self.protocol("WM_DELETE_WINDOW", self.upon_closing_gui)

    # Main GUI Elements ==========================================
    def create_set_shortcuts_elements(self):
        """Create all of the GUI Elements"""

        # overall gui frame ===========================
        self.inputs_frame = customtkinter.CTkFrame(self)
        self.inputs_frame.grid(**self.inputs_frame_dict)

        # url

        self.url_label = customtkinter.CTkLabel(self.inputs_frame, text="Youtube URL:")
        self.url_label.grid(**self.url_label_dict)

        self.url_textvar = StringVar()
        self.url_entry = customtkinter.CTkEntry(
            self.inputs_frame,
            placeholder_text="Youtube URL",
            textvariable=self.url_textvar,
        )
        self.url_entry.grid(**self.url_entry_dict)

        # File
        self.filepath_label = customtkinter.CTkLabel(self.inputs_frame, text="Filepath:")
        self.filepath_label.grid(**self.filepath_label_dict)

        self.file_textvar = StringVar()
        self.file_entry = customtkinter.CTkEntry(
            self.inputs_frame,
            placeholder_text="Video Filepath",
            textvariable=self.file_textvar,
        )
        self.file_entry.grid(**self.file_entry_dict)

        # Name
        self.name_label = customtkinter.CTkLabel(self.inputs_frame, text="Name:")
        self.name_label.grid(**self.name_label_dict)

        self.name_textvar = StringVar()
        self.name_entry = customtkinter.CTkEntry(
            self.inputs_frame,
            placeholder_text="Name",
            textvariable=self.name_textvar,
        )
        self.name_entry.grid(**self.name_entry_dict)

        # Start Time
        self.start_label = customtkinter.CTkLabel(self.inputs_frame, text="Start Time:")
        self.start_label.grid(**self.start_label_dict)
        self.start_var = StringVar()
        self.start_entry = customtkinter.CTkEntry(
            self.inputs_frame,
            placeholder_text="Start Time",
            textvariable=self.start_var,
        )
        self.start_entry.grid(**self.start_entry_dict)

        # End Time
        self.end_label = customtkinter.CTkLabel(self.inputs_frame, text="End Time:")
        self.end_label.grid(**self.end_label_dict)
        self.end_var = StringVar()
        self.end_entry = customtkinter.CTkEntry(
            self.inputs_frame,
            placeholder_text="End Time",
            textvariable=self.end_var,
        )
        self.end_entry.grid(**self.end_entry_dict)

        # Cover photo time
        self.cover_label = customtkinter.CTkLabel(self.inputs_frame, text="Cover Photo Time:")
        self.cover_label.grid(**self.cover_label_dict)
        self.cover_var = StringVar()
        self.cover_entry = customtkinter.CTkEntry(
            self.inputs_frame,
            placeholder_text="Cover Photo Time",
            textvariable=self.cover_var,
        )
        self.cover_entry.grid(**self.cover_entry_dict)

        # Speed
        self.speed_label = customtkinter.CTkLabel(self.inputs_frame, text="Speed")
        self.speed_label.grid(**self.speed_label_dict)
        self.speed_var = StringVar()
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
            command=self.enter_last_values,  # Command to be called if user wants last values
        )
        self.last_values_btn.grid(**self.last_values_btn_dict)

        # Confirm Button
        self.entry_confirm_btn = customtkinter.CTkButton(
            master=self.inputs_frame,
            text="Confirm",
            # fg_color="green2",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.gather_user_input_and_close,  # Command to be called if user confirms
        )
        self.entry_confirm_btn.grid(**self.entry_confirm_btn_dict)

    def enter_last_values(self):
        """Fetch last job values and populate to GUI"""

        # get last values
        self.job.retrieve_last_params_from_file()
        self.raw_gui_video_params = self.job.raw_video_params
        if not any(self.raw_gui_video_params):
            print("No last values found")

        else:
            url = self.raw_gui_video_params["url"]
            filepath = self.raw_gui_video_params["filepath"]
            # name = self.raw_gui_video_params["name"]
            start = self.raw_gui_video_params["start"]
            end = self.raw_gui_video_params["end"]
            cover = self.raw_gui_video_params["cover"]
            speed = self.raw_gui_video_params["speed"]

            # populate last values
            self.url_textvar.set(url)
            self.file_textvar.set(filepath)
            # self.name_textvar.set(name)
            if start and float(start):
                self.start_var.set(start)
            if end and float(end):
                self.end_var.set(end)
            if cover and float(cover):
                self.cover_var.set(cover)
            if speed and float(speed):
                self.speed_var.set(speed)

            # refresh gui
            self.update()

    def gather_user_input_and_close(self):
        """Extract user entered gui information for a video job"""
        self.raw_gui_video_params["url"] = self.url_entry.get()
        self.raw_gui_video_params["filepath"] = self.file_entry.get()
        self.raw_gui_video_params["name"] = self.name_entry.get()
        self.raw_gui_video_params["start"] = self.start_entry.get()
        self.raw_gui_video_params["end"] = self.end_entry.get()
        self.raw_gui_video_params["cover"] = self.cover_entry.get()
        self.raw_gui_video_params["speed"] = self.speed_entry.get()

        # Close
        self.withdraw()
        self.quit()

        print("Confirmed", flush=True)

    def execute_gui(self):
        """Run the gui and return the inputs"""
        self.mainloop()
        # self.quit()
        return self.user_quit, self.raw_gui_video_params

    def upon_closing_gui(self):
        """Action to be taken if user Xs out of gui"""
        self.user_quit = True
        # print("User chose to exit GUI", flush=True)
        print("User exited GUI")
        self.withdraw()
        self.quit()

        print("Exiting", flush=True)


if __name__ == "__main__":
    from video_processor.media import Job

    VideoJobGui(Job()).execute_gui()
