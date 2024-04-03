from customtkinter import (CTkFrame,
                           StringVar,
                           IntVar,
                           BooleanVar,
                           DoubleVar,
                           filedialog)
from .customclasses import (Button,
                            CheckBox,
                            ComboBox,
                            RadioButton,
                            NormalFrame,
                            Entry,
                            Label,
                            ClassTable,
                            Slider,
                            LogFrame,
                            LoadModelFrame,
                            ColImage)
from appstate import AppState

class ConsciousFrame(CTkFrame):

    def __init__(self, master, *args, **kwargs):

        super().__init__(master, width=0, height=0, *args, **kwargs)
        self.state = ''
        self.max_rows = 0

        self.input_delay = StringVar(self, AppState.get_attr('delay'))
        self.video_path = StringVar(self, value=AppState.get_attr('video_path'))
        self.osc_port = StringVar(self, value=AppState.get_attr('osc_port'))
        self.max_freq = StringVar(self, value=AppState.get_attr('max_frequency'))
        self.input_duration = StringVar(self, value=AppState.get_attr('duration'))
        self.webcam_active = BooleanVar(self, value=AppState.get_attr('webcam_active'))
        self.webcam_index = StringVar(self, value=AppState.get_attr('webcam_index'))
        self.train_epochs = StringVar(self, value=AppState.get_attr('epochs'))
        self.target_loss = StringVar(self, value=AppState.get_attr('target_loss'))
        self.test_split = DoubleVar(self, value=AppState.get_attr('test_split'))
        self.classification_output = StringVar(self, value=AppState.get_attr('class_output'))

        self.left = NormalFrame(self)
        self.left.pack(side='left', anchor='sw')
        self.right = NormalFrame(self)
        self.pad = NormalFrame(self)
        self.pad.pack(side='right', expand=False, anchor='e', fill='y')
        Label(self.pad, text=' ').pack(side='right')
        self.right.pack(side='right', expand=True, anchor='sw', fill='both')
        self.right.columnconfigure(3, weight=1)

        self.input_settings_frame = NormalFrame(self.right)
        self.class_table = ClassTable(self.right)
        self.load_model_frame = LoadModelFrame(self.right, refresh=None)

        self.input_delay_entry = Entry(self.input_settings_frame, width=36, textvariable=self.input_delay)
        self.input_duration_entry = Entry(self.input_settings_frame, width=36, textvariable=self.input_duration)
        self.webcam_index_entry = Entry(self.input_settings_frame, width=36, textvariable=self.webcam_index)
        self.classification_output_select = ComboBox(self.right, values=AppState._classification_outputs, variable=self.classification_output)
        self.send_pose_data = CheckBox(self.right, text='Send Pose Data')
        self.display_input = CheckBox(self.right, text='Input')
        self.display_pose = CheckBox(self.right, text='Pose')
        self.use_cuda = CheckBox(self.right, text='CUDA')
        self.use_regularization = CheckBox(self.right, text='Pose')

        self.osc_port_entry = Entry(self.right, width=54, textvariable=self.osc_port)
        self.max_freq_entry = Entry(self.right, width=36, textvariable=self.max_freq)
        self.train_epochs_entry = Entry(self.right, width=36, textvariable=self.train_epochs)
        self.target_loss_entry = Entry(self.right, textvariable=self.target_loss)
        self.test_split_label = Label(self.right, text=AppState.get_attr('test_split'))
        self.new_gesture_entry = Entry(self.right, width=0, placeholder_text='')
        self.new_model_entry = Entry(self.right, width=0, placeholder_text='')
        self.new_model_button = Button(self.right, type='ACTION', text='New Model', fct=self.new_model)

        self.new_gesture_button = Button(self.right, text='Add Gesture', type='ACTION', fct=self.add_gesture)
        self.video_path_button = Button(self.input_settings_frame, text=self.formatted_video_path(), type='ACTION', fct=self.browse_video_path)
        self.webcam_rb = RadioButton(self.right, text='Webcam', command=self.set_input_webcam)
        self.video_rb = RadioButton(self.right, text='Video', command=self.set_input_video)
        self.test_split_slider = Slider(self.right, from_=0, to=100, number_of_steps=400, command=self.test_split_callback, variable=self.test_split)

        self.home_img = ColImage(self.left, path='UI/Assets/home.png', size=(150, 263), color=self.test_split_label.cget('text_color'))
        self.move_img = ColImage(self.left, path='UI/Assets/move.png', size=(150, 214), color=self.test_split_label.cget('text_color'))
        self.rec_img = ColImage(self.left, path='UI/Assets/rec.png', size=(150, 165), color=self.test_split_label.cget('text_color'))
        self.train_img = ColImage(self.left, path='UI/Assets/train.png', size=(150, 165), color=self.test_split_label.cget('text_color'))

        for i in range(4):
            self.columnconfigure(i, weight=1)

    def state(self, name):
        return self.state == name
    
    def spreadrows(self, rows):
        self.max_rows = max(self.max_rows, rows)
        '''for i in range(self.max_rows):
            self.right.rowconfigure(i, weight=int(i<rows), uniform='a')'''
    
    def clearFrame(self, state=''):
        if self.state==state:
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
        self.video_path.set(filedialog.askopenfilenames(initialdir = '/', title = 'Select File', filetypes = (('csv files', '*.csv'),('all files', '*.*')))[0])
        self.video_path_button.configure(text=self.formatted_video_path())

    def formatted_video_path(self):
        max_length=36
        path = self.video_path.get()
        return '. . . '+path[-1*(max_length-3):] if len(path) > max_length else path

      
    def set_input_video(self):
        if self.webcam_active.get():
            self.webcam_active.set(False)
            self.webcam_rb.deactivate()
            Label(self.input_settings_frame, text="Delay").grid(row=0, column=0, sticky='w')
            self.input_delay_entry.grid(row=0, column=1, sticky='w')
            Label(self.input_settings_frame, text='Source').grid(row=0, column=2, sticky='nesw')
            self.video_path_button.grid(row=0, column=3, columnspan=3, sticky='ew')

    def set_input_webcam(self):
        if not self.webcam_active.get():
            self.webcam_active.set(True)
            self.video_rb.deactivate()
            Label(self.input_settings_frame, text="Delay").grid(row=0, column=0, sticky='w')
            self.input_delay_entry.grid(row=0, column=1, sticky='w')
            Label(self.input_settings_frame, text="Duration").grid(row=0, column=2, sticky='w')
            self.input_duration_entry.grid(row=0, column=3, sticky='w')
            Label(self.input_settings_frame, text="Index").grid(row=0, column=4, sticky='w')
            self.webcam_index_entry.grid(row=0, column=5, sticky='w')
        try:
            self.video_path_button.destroy()
            self.video_path_button = Button(self.input_settings_frame, text=self.formatted_video_path(), type='ACTION', fct=self.browse_video_path)
        except:
            pass

    def test_split_callback(self, value):
        self.test_split_label.configure(text=f'{value}%')

    def drawHomeFrame(self):

        if(self.clearFrame('home')):
            row = 0
            left = self.left
            right = self.right
            self.home_img.pack(side='top', anchor ='n', fill='y')

            self.new_model_entry.grid(row=0, column=0, columnspan=2, sticky='nesw', pady=8)
            self.new_model_button.grid(row=1, column=0, columnspan=2, sticky='nesw')
            Label(right, text=' ').grid(row=6, column=2)
            self.load_model_frame.grid(column=3, columnspan=1, row=0, rowspan=7, sticky='new', pady=8)
            Label(right, text='Current Model').grid(row=2, column=0, columnspan=2, sticky='w')
            i=3
            info = AppState.active_model_info()
            if info is None:
                Label(right, 'Create or Load a model').grid(row=i, column=0, columnspan=2)
            else:
                for name, val in info:
                    Label(right, text=name).grid(row=i, column=0, sticky='w')
                    Label(right, text=val).grid(row=i, column=1, sticky='w')
                    i+=1

            self.spreadrows(7)

    def drawMoveFrame(self):
        
        if(self.clearFrame('move')):

            left = self.left
            self.move_img.pack(side='top', anchor ='n', fill='y')
            Button(left, type='BIG', text='MOVE').pack(anchor='sw', side='bottom')
            right = self.right

            row = 0

            Label(right, text='Input').grid(row=row, column=0, columnspan=1, sticky='w')
            self.webcam_rb.grid(row=row, column=1, sticky='w')
            self.video_rb.grid(row=row, column=3, sticky='w')
            row+=1

            self.input_settings_frame.grid(row=row, column=0, columnspan=4, sticky='nesw')
            for i in range(6):
                self.input_settings_frame.columnconfigure(i, weight=1)
            if self.webcam_active.get():
                self.webcam_active.set(False)
                self.webcam_rb.invoke()
            else:
                self.webcam_active.set(True)
                self.video_rb.invoke()
            row+=1

            Label(right, text='Output').grid(row=row, column=0, sticky='w')
            self.classification_output_select.grid(row=row, column=1, columnspan=2, sticky='w')
            if AppState.get_attr('send_pose')!=self.send_pose_data.get():
                self.send_pose_data.toggle()
            self.send_pose_data.grid(row=row, column=2, columnspan=2, sticky='e')
            row+=1

            Label(right, text='Display').grid(row=row, column=0, sticky='w')
            self.display_input.grid(row=row, column=1, columnspan=1, sticky='')
            if AppState.get_attr('show')!=self.display_input.get():
                self.display_input.toggle()
            self.display_pose.grid(row=row, column=3, columnspan=1, sticky='w')
            if AppState.get_attr('show_pose')!=self.display_pose.get():
                self.display_pose.toggle()
            row+=1

            Label(right, text='OSC Port').grid(row=row, column=0, sticky='w')
            self.osc_port_entry.grid(row=row, column=1, sticky='w')
            Label(right, text='Max Freq').grid(row=row, column=2, sticky='w')
            self.max_freq_entry.grid(row=row, column=3, sticky='')

            self.spreadrows(row)

    def drawTraceFrame(self):
        
        if(self.clearFrame('record')):
            
            left = self.left
            Button(left, type='BIG', text='RECORD').pack(anchor='sw', side='bottom')
            Button(left, type='BIG', text='UNDO').pack(anchor='sw', side='bottom')
            right = self.right
            self.rec_img.pack(side='top', anchor ='n', fill='y')

            row = 0

            Label(right, text='Input').grid(row=row, column=0, columnspan=1, sticky='w')
            self.webcam_rb.grid(row=row, column=1, sticky='w')
            self.video_rb.grid(row=row, column=3, sticky='')
            row+=1
            
            self.input_settings_frame.grid(row=row, column=0, columnspan=4, sticky='nesw')
            for i in range(6):
                self.input_settings_frame.columnconfigure(i, weight=1)
            if self.webcam_active.get():
                self.webcam_active.set(False)
                self.webcam_rb.invoke()
            else:
                self.webcam_active.set(True)
                self.video_rb.invoke()
            row+=1

            Label(right, text='Name').grid(row=row, column=0, columnspan=1, sticky='w')
            self.new_gesture_entry.grid(row=row, column=1, columnspan=2, sticky='ew', padx=3)
            self.new_gesture_button.grid(row=row, column=3, sticky='ew')
            row+=1

            self.class_table.grid(row=row, rowspan=2, column=0, columnspan=4, sticky='nesw', ipadx=5)

            right.rowconfigure(row, weight=0)

            self.spreadrows(row)

    def drawTrainFrame(self):
        
        if(self.clearFrame('train')):
            left = self.left
            Button(left, type='BIG', text='TRAIN').pack(anchor='sw', side='bottom')
            Button(left, type='BIG', text='STOP').pack(anchor='sw', side='bottom')
            right = self.right
            self.train_img.pack(side='top', anchor ='n', fill='y')

            row = 0

            Label(right, text='Epochs').grid(row=row, column=0, columnspan=1, sticky='w')
            self.train_epochs_entry.grid(row=row, column=1, sticky='w')
            Label(right, text='Target Loss').grid(row=row, column=2, columnspan=1, sticky='e')
            self.target_loss_entry.grid(row=row, column=3, sticky='w')
            row+=1
            
            Label(right, text='Test Split').grid(row=row, column=0, columnspan=1, sticky='w')
            self.test_split_label.grid(row=row, column=3, columnspan=1, sticky='e')
            self.test_split_slider.grid(row=row, column=1, columnspan=3, sticky = 'w')
            #self.test_split_callback(self.test_split.get())

            row+=1

            self.use_cuda.grid(row=row, column=1, columnspan=1, sticky='w')
            if AppState.get_attr('cuda') != self.use_cuda.get():
                self.use_cuda.toggle()
            if AppState.get_attr('regularization') != self.use_regularization.get():
                self.use_regularization.toggle()
            self.use_regularization.grid(row=row, column=3, columnspan=1, sticky='w')
            row+=1

            self.logs_frame = LogFrame(right)
            self.logs_frame.grid(row=row, rowspan=2, column=0, columnspan=4, sticky='nesw')

            right.rowconfigure(row, weight=0)

            self.spreadrows(row)

    def set_ui_inputs(self):
        ui_state={'webcam_active': self.webcam_active.get(),
                'webcam_index': int(self.webcam_index.get()),
                'delay': int(self.input_delay.get()),
                'duration': int(self.input_duration.get()),
                'video_path': self.video_path.get(),
                'class_output': self.classification_output.get(),
                'send_pose': self.send_pose_data.get(),
                'show': self.display_input.get(),
                'show_pose': self.display_pose.get(),
                'osc_port': int(self.osc_port.get()),
                'max_frequency': int(self.max_freq.get()),
                'epochs': int(self.train_epochs.get()),
                'target_loss': float(self.target_loss.get()),
                'test_split': float(self.test_split.get()),
                'cuda': self.use_cuda.get(),
                'regularization': self.use_regularization.get()}
        AppState.set_ui_state(ui_state)

    def get_ui_inputs(self):
        self.input_delay.set(AppState.get_attr('delay'))
        self.video_path.set(AppState.get_attr('video_path'))
        self.osc_port.set(AppState.get_attr('osc_port'))
        self.max_freq.set(AppState.get_attr('max_frequency'))
        self.input_duration.set(AppState.get_attr('duration'))
        self.webcam_active.set(AppState.get_attr('webcam_active'))
        self.webcam_index.set(AppState.get_attr('webcam_index'))
        self.classification_output.set(AppState.get_attr('class_output'))
        self.test_split.set(AppState.get_attr('test_split'))

    def add_gesture(self):
        self.class_table.add_gesture(self.new_gesture_entry.get())

    def new_model(self):
        pass

    def log(self, msg):
        self.logs_frame.update(msg)