from customtkinter import CTkFrame, StringVar, BooleanVar, DoubleVar, filedialog
from .customclasses import (
    Button,
    CheckBox,
    ComboBox,
    RadioButton,
    NormalFrame,
    Entry,
    Label,
    Log,
    ClassTable,
    Slider,
    LogFrame,
    LoadModelFrame,
    ModelInfoFrame,
    ColImage,
)
from appstate import AppState
from ENGINE.engine import Engine
from ENGINE.tasks import Tasks
from ENGINE.trainer import Trainer
from taskmanager import TaskManager
from listener import OSCControlServer
import asyncio


class ConsciousFrame(CTkFrame):

    def __init__(self, master, *args, **kwargs):

        super().__init__(master, width=0, height=0, *args, **kwargs)
        self.state = ""
        self.max_rows = 0

        self.input_delay = StringVar(self, AppState.get_attr("delay"))
        self.video_path = StringVar(self, value=AppState.get_attr("video_path"))
        self.osc_ip = StringVar(self, value=AppState.get_attr("osc_ip"))
        self.osc_port = StringVar(self, value=AppState.get_attr("osc_port"))
        self.osc_address = StringVar(self, value=AppState.get_attr("osc_address"))
        self.listen_port = StringVar(self, value=AppState.get_attr("listen_port"))
        self.input_duration = StringVar(self, value=AppState.get_attr("duration"))
        self.webcam_active = BooleanVar(self, value=AppState.get_attr("webcam_active"))
        self.webcam_index = StringVar(self, value=AppState.get_attr("webcam_index"))
        self.train_epochs = StringVar(self, value=AppState.get_attr("epochs"))
        self.learn_rate = DoubleVar(self, value=AppState.get_attr("learn_rate"))
        self.temporal_size = StringVar(self, value=AppState.get_attr("temporal_size"))
        self.batch_size = StringVar(self, value=AppState.get_attr("batch_size"))
        self.test_split = DoubleVar(self, value=AppState.get_attr("test_split"))
        self.x_loc = DoubleVar(self, value=AppState.get_attr("x_loc"))
        self.y_loc = DoubleVar(self, value=AppState.get_attr("y_loc"))
        self.x_size = DoubleVar(self, value=AppState.get_attr("x_size"))
        self.y_size = DoubleVar(self, value=AppState.get_attr("y_size"))
        self.momentum = DoubleVar(self, value=AppState.get_attr("momentum"))
        self.conf_threshold = DoubleVar(self, value=AppState.get_attr("conf_threshold"))
        self.classification_output = StringVar(
            self, value=AppState.get_attr("class_output")
        )

        self.left = NormalFrame(self)
        self.left.pack(side="left", anchor="sw", fill="y")
        self.right = NormalFrame(self)
        self.pad = NormalFrame(self)
        self.pad.pack(side="right", expand=False, anchor="e", fill="y")
        Label(self.pad, text=" ").pack(side="right")
        self.right.pack(
            side="right", expand=True, anchor="sw", fill="both", padx=0, pady=0
        )
        self.right.columnconfigure(3, weight=1)

        self.input_settings_frame = NormalFrame(self.right)
        self.input_settings_frame.columnconfigure([i for i in range(5)], weight=1)
        self.osc_settings_frame = NormalFrame(self.right)
        self.osc_settings_frame.columnconfigure(index=[i for i in range(5)], weight=1)
        self.class_table = ClassTable(self.right)
        self.load_model_frame = LoadModelFrame(self.right, refresh=self.redrawHome)
        self.model_info_frame = ModelInfoFrame(self.right)

        self.input_delay_entry = Entry(
            self.input_settings_frame, width=54, textvariable=self.input_delay
        )
        self.input_duration_entry = Entry(
            self.input_settings_frame, width=54, textvariable=self.input_duration
        )
        self.webcam_index_entry = Entry(
            self.input_settings_frame, width=54, textvariable=self.webcam_index
        )
        self.batch_size_entry = Entry(
            self.right, width=54, textvariable=self.batch_size
        )
        self.learn_rate_select = ComboBox(
            self.right,
            values=[str(val) for val in AppState._learn_rates],
            variable=self.learn_rate,
        )
        self.custom_size = CheckBox(self.right, text="Custom Window Size")
        self.send_pose_data = CheckBox(self.right, text="Send Pose Data")
        self.display_input = CheckBox(self.right, text="Input")
        if AppState.get_attr("show") != self.display_input.get():
            self.display_input.toggle()
        self.display_pose = CheckBox(self.right, text="Pose")
        if AppState.get_attr("show_pose") != self.display_pose.get():
            self.display_pose.toggle()
        self.use_cuda = CheckBox(self.right, text="CUDA")
        self.use_regularization = CheckBox(self.right, text="Pose")

        self.listen_port_entry = Entry(
            self.right, width=54, textvariable=self.listen_port
        )
        self.osc_ip_entry = Entry(
            self.osc_settings_frame, width=108, textvariable=self.osc_ip
        )
        self.osc_port_entry = Entry(
            self.osc_settings_frame, width=54, textvariable=self.osc_port
        )
        self.osc_address_entry = Entry(
            self.osc_settings_frame, width=54, textvariable=self.osc_address
        )
        Label(self.osc_settings_frame, text="OSC Output [ Ip, Port, Adress ]").grid(
            row=0, column=0, columnspan=2, sticky="w"
        )
        self.osc_ip_entry.grid(row=0, column=2, sticky="ew")
        self.osc_port_entry.grid(row=0, column=3, sticky="ew", padx=8)
        self.osc_address_entry.grid(row=0, column=4, sticky="ew")

        self.train_epochs_entry = Entry(
            self.right, width=54, textvariable=self.train_epochs
        )
        self.temporal_size_entry = Entry(
            self.right, width=54, textvariable=self.temporal_size
        )
        self.test_split_label = Log(self.right, text=f"{self.test_split.get():.1f}%", anchor="e")
        self.x_loc_label = Log(self.right, text=f"{self.x_loc.get():.1f}%", anchor="e")
        self.y_loc_label = Log(self.right, text=f"{self.y_loc.get():.1f}%", anchor="e")
        self.x_size_label = Log(self.right, text=f"{self.x_size.get():.1f}%", anchor="e")
        self.y_size_label = Log(self.right, text=f"{self.y_size.get():.1f}%", anchor="e")
        self.momentum_label = Log(self.right, text=f"{self.momentum.get():.2f}", anchor="e")
        self.conf_threshold_label = Log(
            self.right, text=f"{self.conf_threshold.get():.2f}", anchor="e"
        )
        self.new_gesture_entry = Entry(self.right, width=0, placeholder_text="")
        self.new_model_entry = Entry(self.right, width=0, placeholder_text="")
        self.new_model_button = Button(
            self.right, type="ACTION", text="New Model", command=self.new_model
        )
        self.delete_model_button = Button(
            self.right, type="ACTION", text="Delete", command=self.delete_model
        )
        self.copy_model_button = Button(
            self.right, type="ACTION", text="Copy Active", command=self.copy_model
        )
        self.export_model_button = Button(
            self.right, type="ACTION", text="Export", command=self.export_model
        )
        self.import_model_button = Button(
            self.right, type="ACTION", text="Import As", command=self.import_model
        )
        self.restore_deleted_button = Button(
            self.right, type="ACTION", text="Restore", command=self.restore_deleted
        )

        self.new_gesture_button = Button(
            self.right, text="Add Gesture", type="ACTION", command=self.add_gesture
        )
        self.video_path_button = Button(
            self.input_settings_frame,
            text=self.formatted_video_path(),
            type="ACTION",
            command=self.browse_video_path,
        )
        self.listen_server_button = Button(
            self.right,
            text="Start Listening Server",
            type="ACTION",
            command=self.start_listening,
        )
        self.webcam_rb = RadioButton(
            self.right, text="Webcam", command=self.set_input_webcam
        )
        self.video_rb = RadioButton(
            self.right, text="Video", command=self.set_input_video
        )
        self.test_split_slider = Slider(
            self.right,
            from_=0,
            to=100,
            number_of_steps=200,
            command=self.test_split_callback,
            variable=self.test_split,
        )
        self.x_loc_slider = Slider(
            self.right,
            from_=0,
            to=100,
            number_of_steps=200,
            command=self.x_loc_callback,
            variable=self.x_loc,
        )
        self.y_loc_slider = Slider(
            self.right,
            from_=0,
            to=100,
            number_of_steps=200,
            command=self.y_loc_callback,
            variable=self.y_loc,
        )
        self.x_size_slider = Slider(
            self.right,
            from_=0,
            to=100,
            number_of_steps=200,
            command=self.x_size_callback,
            variable=self.x_size,
        )
        self.y_size_slider = Slider(
            self.right,
            from_=0,
            to=100,
            number_of_steps=200,
            command=self.y_size_callback,
            variable=self.y_size,
        )
        self.momentum_slider = Slider(
            self.right,
            from_=0,
            to=0.50,
            number_of_steps=50,
            command=self.momentum_callback,
            variable=self.momentum,
        )
        self.conf_threshold_slider = Slider(
            self.right,
            from_=0,
            to=0.25,
            number_of_steps=25,
            command=self.conf_threshold_callback,
            variable=self.conf_threshold,
        )

        self.home_img = ColImage(
            self.left,
            path="UI/Assets/home.png",
            size=(150, 450),
            color=self.test_split_label.cget("text_color"),
        )
        self.move_img = ColImage(
            self.left,
            path="UI/Assets/move.png",
            size=(150, 410),
            color=self.test_split_label.cget("text_color"),
        )
        self.rec_img = ColImage(
            self.left,
            path="UI/Assets/rec.png",
            size=(150, 360),
            color=self.test_split_label.cget("text_color"),
        )
        self.train_img = ColImage(
            self.left,
            path="UI/Assets/train.png",
            size=(150, 310),
            color=self.test_split_label.cget("text_color"),
        )

        for i in range(4):
            self.columnconfigure(i, weight=1)

    def state(self, name):
        return self.state == name

    def clearFrame(self, state=""):
        if self.state == state:
            return False
        self.state = state
        self.set_ui_inputs()
        for widget in self.input_settings_frame.winfo_children():
            widget.grid_forget()
        for widget in self.right.winfo_children():
            widget.grid_forget()
        for widget in self.left.winfo_children():
            widget.pack_forget()
        return True

    def browse_video_path(self):
        file_types = [
            (
                "All video files",
                "*.mp4 *.avi *.mkv *.mov *.flv *.wmv *.m4v *.mpeg *.mpg",
            ),
            ("MP4 files", "*.mp4"),
            ("AVI files", "*.avi"),
            ("MKV files", "*.mkv"),
            ("MOV files", "*.mov"),
            ("FLV files", "*.flv"),
            ("WMV files", "*.wmv"),
            ("M4V files", "*.m4v"),
            ("MPEG files", "*.mpeg *.mpg"),
            ("All files", "*.*"),
        ]
        filenames = filedialog.askopenfilenames(
            initialdir="/", title="Select File", filetypes=file_types
        )
        if len(filenames) > 0:
            self.video_path.set(filenames[0])
            self.video_path_button.configure(text=self.formatted_video_path())

    def formatted_video_path(self):
        max_length = 36
        path = self.video_path.get()
        return (
            ". . . " + path[-1 * (max_length - 3) :] if len(path) > max_length else path
        )

    def set_input_video(self):
        if self.webcam_active.get():
            for widget in self.input_settings_frame.winfo_children():
                widget.grid_forget()
            self.webcam_active.set(False)
            self.webcam_rb.deactivate()
            Label(self.input_settings_frame, text="Delay").grid(
                row=0, column=0, sticky="w"
            )
            self.input_delay_entry.grid(row=0, column=1, sticky="w")
            Label(self.input_settings_frame, text="Source").grid(
                row=0, column=2, sticky="w"
            )
            self.video_path_button.grid(row=0, column=3, columnspan=2, sticky="we")

    def set_input_webcam(self):
        if not self.webcam_active.get():
            for widget in self.input_settings_frame.winfo_children():
                widget.grid_forget()
            self.webcam_active.set(True)
            self.video_rb.deactivate()
            Label(self.input_settings_frame, text="Delay").grid(
                row=0, column=0, sticky="w"
            )
            self.input_delay_entry.grid(row=0, column=0, sticky="e")
            Label(self.input_settings_frame, text="Duration").grid(
                row=0, column=2, sticky="w"
            )
            self.input_duration_entry.grid(row=0, column=2, sticky="e")
            Label(self.input_settings_frame, text="Index").grid(
                row=0, column=4, sticky="w"
            )
            self.webcam_index_entry.grid(row=0, column=4, sticky="e")
        try:
            self.video_path_button.destroy()
            self.video_path_button = Button(
                self.input_settings_frame,
                text=self.formatted_video_path(),
                type="ACTION",
                command=self.browse_video_path,
            )
        except:
            pass

    def test_split_callback(self, value):
        self.test_split_label.configure(text=f"{value:.1f}%")

    def x_loc_callback(self, value):
        self.x_loc_label.configure(text=f"{value:.1f}%")

    def y_loc_callback(self, value):
        self.y_loc_label.configure(text=f"{value:.1f}%")

    def x_size_callback(self, value):
        self.x_size_label.configure(text=f"{value:.1f}%")

    def y_size_callback(self, value):
        self.y_size_label.configure(text=f"{value:.1f}%")

    def momentum_callback(self, value):
        self.momentum_label.configure(text=f"{value:.2f}")

    def conf_threshold_callback(self, value):
        self.conf_threshold_label.configure(text=f"{value:.2f}")

    def redrawHome(self):
        self.state = ""
        self.drawHomeFrame()

    def drawHomeFrame(self):

        if self.clearFrame("home"):

            self.title()
            self.new_model_entry.clear()

            left = self.left
            right = self.right
            self.home_img.pack(side="top", anchor="nw", fill="both")

            self.new_model_entry.grid(
                row=0, column=0, columnspan=2, sticky="ew", pady=8
            )
            self.new_model_button.grid(
                row=1, column=0, columnspan=1, sticky="ew", padx=(0, 4), pady=0
            )
            self.copy_model_button.grid(
                row=1, column=1, columnspan=1, sticky="ew", padx=(4, 0), pady=0
            )
            self.model_info_frame.grid(
                row=2, rowspan=4, column=0, columnspan=2, sticky="nesw", pady=8
            )
            self.delete_model_button.grid(
                row=6, column=0, columnspan=1, sticky="ew", padx=(0, 4), pady=0
            )
            self.restore_deleted_button.grid(
                row=6, column=1, columnspan=1, sticky="ew", padx=(4, 0), pady=0
            )

            self.load_model_frame.grid(
                column=3,
                columnspan=1,
                row=0,
                rowspan=5,
                sticky="new",
                pady=8,
                padx=(8, 0),
            )
            self.import_model_button.grid(
                row=5, column=3, columnspan=1, sticky="ew", pady=(0, 8), padx=(8, 0)
            )
            self.export_model_button.grid(
                row=6, column=3, columnspan=1, sticky="ew", padx=(8, 0)
            )

    def drawMoveFrame(self):

        if self.clearFrame("move"):

            left = self.left
            self.move_img.pack(side="top", anchor="n", fill="y")
            Button(left, type="BIG", text="MOVE", command=self.move).pack(
                anchor="sw", side="bottom"
            )
            right = self.right

            row = 0

            Label(right, text="Input").grid(row=row, column=0, columnspan=1, sticky="w")
            self.webcam_rb.grid(row=row, column=1, sticky="w")
            self.video_rb.grid(row=row, column=3, sticky="w")
            row += 1

            self.input_settings_frame.grid(
                row=row, column=0, columnspan=4, sticky="nesw"
            )
            if self.webcam_active.get():
                self.webcam_active.set(False)
                self.webcam_rb.invoke()
            else:
                self.webcam_active.set(True)
                self.video_rb.invoke()
            row += 1

            Label(right, text="Display").grid(row=row, column=0, sticky="w")
            self.display_input.grid(row=row, column=1, columnspan=1, sticky="w")
            if AppState.get_attr("show") != self.display_input.get():
                self.display_input.toggle()
            self.display_pose.grid(row=row, column=2, columnspan=1, sticky="w")
            if AppState.get_attr("show_pose") != self.display_pose.get():
                self.display_pose.toggle()
            self.custom_size.grid(row=row, column=3, sticky="w")
            row += 1

            Label(right, text="X Size").grid(
                row=row, column=0, columnspan=1, sticky="w"
            )
            self.x_size_label.grid(row=row, column=3, columnspan=1, sticky="e")
            self.x_size_slider.grid(
                row=row, column=1, columnspan=3, sticky="ew"
            )
            row += 1

            Label(right, text="Y Size").grid(
                row=row, column=0, columnspan=1, sticky="w"
            )
            self.y_size_label.grid(row=row, column=3, columnspan=1, sticky="e")
            self.y_size_slider.grid(
                row=row, column=1, columnspan=3, sticky="ew"
            )
            row += 1

            Label(right, text="X Loc").grid(row=row, column=0, columnspan=1, sticky="w")
            self.x_loc_label.grid(row=row, column=3, columnspan=1, sticky="e")
            self.x_loc_slider.grid(
                row=row, column=1, columnspan=3, sticky="ew"
            )
            row += 1

            Label(right, text="Y Loc").grid(row=row, column=0, columnspan=1, sticky="w")
            self.y_loc_label.grid(row=row, column=3, columnspan=1, sticky="e")
            self.y_loc_slider.grid(
                row=row, column=1, columnspan=3, sticky="ew"
            )
            row += 1

            Label(right, text="Momentum").grid(row=row, column=0, sticky="w")
            self.momentum_label.grid(row=row, column=3, columnspan=1, sticky="e")
            self.momentum_slider.grid(
                row=row, column=1, columnspan=3, sticky="ew"
            )
            row += 1

            Label(right, text="CT").grid(row=row, column=0, sticky="w")
            self.conf_threshold_label.grid(row=row, column=3, columnspan=1, sticky="e")
            self.conf_threshold_slider.grid(
                row=row, column=1, columnspan=3, sticky="ew"
            )
            row += 1

            self.osc_settings_frame.grid(row=row, column=0, columnspan=4, sticky="nesw")
            row += 1

            Label(right, text="OSC Listening Server [ Port ]").grid(
                row=row, column=0, columnspan=2, sticky="w"
            )
            self.listen_port_entry.grid(row=row, column=2, sticky="ew")
            self.listen_server_button.grid(row=row, column=3, sticky="ew", padx=(8, 0))

    def drawTraceFrame(self):

        if self.clearFrame("record"):

            left = self.left
            Button(left, type="BIG", text="RECORD", command=self.record).pack(
                anchor="sw", side="bottom"
            )
            Button(left, type="BIG", text="UNDO", command=self.undo_record).pack(
                anchor="sw", side="bottom"
            )
            right = self.right
            self.rec_img.pack(side="top", anchor="n", fill="y")

            row = 0

            Label(right, text="Input").grid(row=row, column=0, columnspan=1, sticky="w")
            self.webcam_rb.grid(row=row, column=1, sticky="w")
            self.video_rb.grid(row=row, column=3, sticky="")
            row += 1

            self.input_settings_frame.grid(
                row=row, column=0, columnspan=4, sticky="nesw"
            )
            if self.webcam_active.get():
                self.webcam_active.set(False)
                self.webcam_rb.invoke()
            else:
                self.webcam_active.set(True)
                self.video_rb.invoke()
            row += 1

            Label(right, text="Display").grid(row=row, column=0, sticky="w")
            self.display_input.grid(row=row, column=1, columnspan=1, sticky="e")
            if AppState.get_attr("show") != self.display_input.get():
                self.display_input.toggle()
            self.display_pose.grid(row=row, column=3, columnspan=1, sticky="")
            if AppState.get_attr("show_pose") != self.display_pose.get():
                self.display_pose.toggle()
            row += 1

            Label(right, text="Momentum").grid(row=row, column=0, sticky="w")
            self.momentum_label.grid(row=row, column=3, columnspan=1, sticky="e")
            self.momentum_slider.grid(
                row=row, column=1, columnspan=3, sticky="ew"
            )
            row += 1

            Label(right, text="CT").grid(row=row, column=0, sticky="w")
            self.conf_threshold_label.grid(row=row, column=3, columnspan=1, sticky="e")
            self.conf_threshold_slider.grid(
                row=row, column=1, columnspan=3, sticky="ew"
            )
            row += 1

            self.new_gesture_entry.grid(
                row=row, column=0, columnspan=3, sticky="ew", padx=(0, 8)
            )
            self.new_gesture_button.grid(row=row, column=3, sticky="ew")
            row += 1

            self.class_table.grid(
                row=row,
                rowspan=2,
                column=0,
                columnspan=4,
                sticky="nesw",
                ipadx=5,
                pady=(8, 0),
            )

            right.rowconfigure(row, weight=0)

    def drawTrainFrame(self):

        if self.clearFrame("train"):
            left = self.left
            Button(left, type="BIG", text="TRAIN", command=self.train).pack(
                anchor="sw", side="bottom"
            )
            Button(left, type="BIG", text="STOP", command=AppState.stop_training).pack(anchor="sw", side="bottom")
            right = self.right
            self.train_img.pack(side="top", anchor="n", fill="y")
            Button(left, type="BIG", text="CANCEL", command=AppState.cancel_training).pack(anchor="sw", side="bottom")
            right = self.right
            self.train_img.pack(side="top", anchor="n", fill="y")
            row = 0

            Label(right, text="Epochs").grid(
                row=row, column=0, sticky="w"
            )
            self.train_epochs_entry.grid(row=row, column=1, sticky="e")
            Label(right, text="                ").grid(
                row=row, column=2
            )
            Label(right, text="Batch Size").grid(row=row, column=3, sticky="w")
            self.batch_size_entry.grid(row=row, column=3, sticky="e")
            row += 1

            Label(right, text="Learning Rate").grid(
                row=row, column=0, sticky="w"
            )
            self.learn_rate_select.grid(
                row=row, column=1, sticky="e"
            )
            Label(right, text="                ").grid(
                row=row, column=2
            )
            Label(right, text="Temporal Size").grid(
                row=row, column=3, sticky="w"
            )
            self.temporal_size_entry.grid(
                row=row, column=3, sticky="e"
            )
            row += 1

            Label(right, text="Test Split").grid(
                row=row, column=0, columnspan=1, sticky="w"
            )
            self.test_split_label.grid(row=row, column=3, columnspan=1, sticky="e")
            self.test_split_slider.grid(
                row=row, column=1, columnspan=3, sticky="ew"
            )
            row += 1

            self.logs_frame = LogFrame(right)
            self.logs_frame.grid(
                row=row, rowspan=2, column=0, columnspan=4, sticky="nesw"
            )

            # right.rowconfigure(row, weight=0)

    def set_ui_inputs(self):
        ui_state = {
            "webcam_active": self.webcam_active.get(),
            "webcam_index": int(self.webcam_index.get()),
            "delay": int(self.input_delay.get()),
            "duration": int(self.input_duration.get()),
            "video_path": self.video_path.get(),
            "class_output": self.classification_output.get(),
            "send_pose": self.send_pose_data.get(),
            "show": self.display_input.get(),
            "show_pose": self.display_pose.get(),
            "osc_port": int(self.osc_port.get()),
            "listen_port": int(self.listen_port.get()),
            "epochs": int(self.train_epochs.get()),
            "test_split": float(self.test_split.get()),
            "batch_size": int(self.batch_size.get()),
            "temporal_size": int(self.temporal_size.get()),
            "learn_rate": float(self.learn_rate.get()),
            "conf_threshold": self.conf_threshold.get(),
            "momentum": self.momentum.get(),
            "custom_size": self.custom_size.get(),
            "x_size": self.x_size.get(),
            "y_size": self.y_size.get(),
            "x_loc": self.x_loc.get(),
            "y_loc": self.y_loc.get(),
        }
        AppState.set_ui_state(ui_state)

    def get_ui_inputs(self):
        self.input_delay.set(AppState.get_attr("delay"))
        self.video_path.set(AppState.get_attr("video_path"))
        self.osc_port.set(AppState.get_attr("osc_port"))
        self.listen_port.set(AppState.get_attr("listen_port"))
        self.input_duration.set(AppState.get_attr("duration"))
        self.webcam_active.set(AppState.get_attr("webcam_active"))
        self.webcam_index.set(AppState.get_attr("webcam_index"))
        self.classification_output.set(AppState.get_attr("class_output"))
        self.test_split.set(AppState.get_attr("test_split"))
        self.temporal_size.set(AppState.get_attr("temporal_size"))
        self.batch_size.set(AppState.get_attr("batch_size"))
        self.learn_rate.set(AppState.get_attr("learn_rate"))
        self.display_input.set(AppState.get_attr("show"))
        self.display_pose.set(AppState.get_attr("show_pose"))
        self.send_pose_data.set(AppState.get_attr("send_pose"))
        self.momentum.set(AppState.get_attr("momentum"))
        self.conf_threshold.set(AppState.get_attr("conf_threshold"))
        self.custom_size.set(AppState.get_attr("custom_size"))
        self.x_loc.set(AppState.get_Attr("x_loc"))
        self.y_loc.set(AppState.get_Attr("y_loc"))
        self.x_size.set(AppState.get_attr("x_size"))
        self.y_size.set(AppState.get_attr("y_size"))
        self.use_cuda.set(AppState.get_Attr("cuda"))
        self.use_regularization.set(AppState.get_attr("regularization"))
        self.train_epochs.set(AppState.get_attr("epochs"))

    def add_gesture(self):
        self.class_table.add_gesture(self.new_gesture_entry.get())
        self.new_gesture_entry.clear()

    def new_model(self):
        AppState.new_model(self.new_model_entry.get())
        self.redrawHome()

    def delete_model(self):
        AppState.delete_model()
        self.redrawHome()

    def copy_model(self):
        AppState.copy_model(self.new_model_entry.get())
        self.redrawHome()

    def import_model(self):
        name = self.new_model_entry.get()
        AppState.import_model(name)
        self.redrawHome()

    def export_model(self):
        AppState.export_active_model()

    def restore_deleted(self):
        AppState.restore_deleted()
        self.redrawHome()

    def title(self):
        title = AppState.get_attr("active_model")
        if title is None:
            self.master.title("Load or create a model")
        else:
            self.master.title(f"Terpsichore: {title}")

    def record(self):
        self.set_ui_inputs()
        self.master.withdraw()
        TaskManager.register_task(
            asyncio.create_task(
                Engine.launch(
                    task=Tasks.RECORD, after=lambda: self.after_exec("record")
                )
            )
        )

    def undo_record(self):
        AppState.undo_last_rec()
        self.after_exec("record")

    def move(self):
        self.set_ui_inputs()
        self.master.withdraw()
        TaskManager.register_task(
            asyncio.create_task(
                Engine.launch(task=Tasks.PERFORM, after=lambda: self.after_exec("move"))
            )
        )

    def train(self):
        self.set_ui_inputs()
        AppState.start_train()
        TaskManager.register_task(asyncio.create_task(Trainer.train()))
        TaskManager.register_task(asyncio.create_task(self.logs_frame.listen()))

    def start_listening(self):
        self.set_ui_inputs()
        port = AppState.get_attr("listen_port")
        OSCControlServer.start()
        self.listen_server_button.configure(
            text=f"Listening @ port {port}", command=self.stop_listening
        )

    def stop_listening(self):

        OSCControlServer.stop()
        self.listen_server_button.configure(
            text=f"Start Listening Server", command=self.start_listening
        )

    def after_exec(self, frame: str):
        self.state = ""
        if frame == "home":
            self.drawHomeFrame()
        elif frame == "move":
            self.drawMoveFrame
        elif frame == "record":
            self.drawTraceFrame()
        elif frame == "train":
            self.drawTrainFrame()
        else:
            self.drawHomeFrame()
        self.master.deiconify()

    def log(self, msg):
        self.logs_frame.update(msg)
