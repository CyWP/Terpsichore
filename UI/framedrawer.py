from customtkinter import (CTkFrame,
                           StringVar,
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
                            LogFrame)


class ConsciousFrame(CTkFrame):

    def __init__(self, master, *args, **kwargs):

        super().__init__(master, width=0, height=0, *args, **kwargs)
        self.state = ''
        self.input_delay = StringVar(self, value='0')
        self.video_path = StringVar(self, 'path/to/video')
        self.max_rows = 0
        for i in range(4):
            self.columnconfigure(i, weight=1)

    def state(self, name):
        return self.state == name
    
    def spreadrows(self, rows):
        self.max_rows = max(self.max_rows, rows)
        for i in range(self.max_rows):
            self.right.rowconfigure(i, weight=int(i<rows), uniform='a')
    
    def clearFrame(self, state=''):
        if self.state==state:
            return False
        self.state = state
        for widget in self.winfo_children():
            widget.destroy() 
        return True
    
    def browse_video_path(self):
        self.video_path.set(filedialog.askopenfilenames(initialdir = '/', title = 'Select File', filetypes = (('csv files', '*.csv'),('all files', '*.*')))[0])
        self.video_path_button.configure(text=self.formatted_video_path())

    def formatted_video_path(self):
        max_length=36
        path = self.video_path.get()
        return '. . . '+path[-1*(max_length-3):] if len(path) > max_length else path

      
    def set_input_video(self):
        if self.webcam_active:
            self.webcam_active = False
            self.webcam_rb.deactivate()
            Label(self.input_settings_frame, text="Delay").grid(row=0, column=0, sticky='w')
            self.input_delay_entry = Entry(self.input_settings_frame, width=36, textvariable=self.input_delay)
            self.input_delay_entry.grid(row=0, column=1, sticky='w')
            Label(self.input_settings_frame, text='Source').grid(row=0, column=2, sticky='nesw')
            self.video_path_button = Button(self.input_settings_frame, text=self.formatted_video_path(), type='ACTION', fct=self.browse_video_path)
            self.video_path_button.grid(row=0, column=3, columnspan=3, sticky='ew')

    def set_input_webcam(self):
        if not self.webcam_active:
            self.webcam_active = True
            self.video_rb.deactivate()
            Label(self.input_settings_frame, text="Delay").grid(row=0, column=0, sticky='w')
            self.input_delay_entry = Entry(self.input_settings_frame, width=36, textvariable=self.input_delay)
            self.input_delay_entry.grid(row=0, column=1, sticky='w')
            Label(self.input_settings_frame, text="Duration").grid(row=0, column=2, sticky='w')
            self.input_duration = Entry(self.input_settings_frame, width=36, placeholder_text='0')
            self.input_duration.grid(row=0, column=3, sticky='w')
            Label(self.input_settings_frame, text="Index").grid(row=0, column=4, sticky='w')
            self.webcam_index = Entry(self.input_settings_frame, width=36, placeholder_text='0')
            self.webcam_index.grid(row=0, column=5, sticky='w')
            try:
                self.video_path_button.destroy()
            except:
                pass

    def test_split_callback(self, value):
        self.test_split_label.configure(text=f'{value}%')

    def drawHomeFrame(self):

        if(self.clearFrame('Home')):
            
            self.left = NormalFrame(self)
            left = self.left
            left.pack(side='left', anchor='sw')
            Button(left, type='BIG', text='NEW').pack(anchor='sw', side='bottom')
            Button(left, type='BIG', text='LOAD').pack(anchor='sw', side='bottom')
            Button(left, type='BIG', text='LAST').pack(anchor='sw', side='bottom')
            self.right = NormalFrame(self)
            right = self.right
            right.pack(side='right', expand=True, anchor='sw', fill='both')
            right.columnconfigure(3, weight=1)


    def drawMoveFrame(self):
        
        if(self.clearFrame('Perform')):
            self.left = NormalFrame(self)
            left = self.left
            left.pack(side='left', anchor='sw')
            Button(left, type='BIG', text='MOVE').pack(anchor='sw', side='bottom')
            self.pad = NormalFrame(self)
            self.pad.pack(side='right', anchor='w', fill='y')
            Label(self.pad, text='').pack(side='right')
            self.right = NormalFrame(self)
            right = self.right
            right.pack(side='right', expand=True, anchor='sw', fill='both')
            right.columnconfigure(3, weight=1)

            row = 0

            Label(right, text='Input').grid(row=row, column=0, columnspan=1, sticky='w')
            self.webcam_rb = RadioButton(right, text='Webcam', command=self.set_input_webcam)
            self.webcam_rb.grid(row=row, column=1, sticky='w')
            self.video_rb = RadioButton(right, text='Video', command=self.set_input_video)
            self.video_rb.grid(row=row, column=3, sticky='w')
            row+=1

            self.webcam_active = False
            self.input_settings_frame = NormalFrame(right)
            self.input_settings_frame.grid(row=row, column=0, columnspan=4, sticky='nesw')
            for i in range(6):
                self.input_settings_frame.columnconfigure(i, weight=1)
            self.webcam_rb.invoke()
            row+=1

            Label(right, text='Output').grid(row=row, column=0, sticky='w')
            self.classification_output = ComboBox(right, values=['Integer', 'Softmax', 'One Hot'])
            self.classification_output.grid(row=row, column=1, columnspan=2, sticky='w')
            self.send_pose_data = CheckBox(right, text='Send Pose Data')
            self.send_pose_data.grid(row=row, column=2, columnspan=2, sticky='e')
            row+=1

            Label(right, text='Display').grid(row=row, column=0, sticky='w')
            self.display_input = CheckBox(right, text='Input')
            self.display_input.grid(row=row, column=1, columnspan=1, sticky='')
            self.display_pose = CheckBox(right, text='Pose')
            self.display_pose.grid(row=row, column=3, columnspan=1, sticky='w')
            row+=1

            Label(right, text='OSC Port').grid(row=row, column=0, sticky='w')
            self.osc_port = Entry(right, width=54, placeholder_text='2442')
            self.osc_port.grid(row=row, column=1, sticky='w')
            Label(right, text='Max Freq').grid(row=row, column=2, sticky='w')
            self.max_freq = Entry(right, width=36, placeholder_text='0')
            self.max_freq.grid(row=row, column=3, sticky='')

            self.spreadrows(row)

    def drawTraceFrame(self):
        
        if(self.clearFrame('Record')):
            
            self.left = NormalFrame(self)
            left = self.left
            left.pack(side='left', anchor='sw')
            Button(left, type='BIG', text='RECORD').pack(anchor='sw', side='bottom')
            Button(left, type='BIG', text='UNDO').pack(anchor='sw', side='bottom')
            self.pad = NormalFrame(self)
            self.pad.pack(side='right', anchor='w', fill='y')
            Label(self.pad, text='').pack(side='right')
            self.right = NormalFrame(self)
            right = self.right
            right.pack(side='right', expand=True, anchor='sw', fill='both')
            right.columnconfigure(3, weight=1)

            row = 0

            Label(right, text='Input').grid(row=row, column=0, columnspan=1, sticky='w')
            self.webcam_rb = RadioButton(right, text='Webcam', command=self.set_input_webcam)
            self.webcam_rb.grid(row=row, column=1, sticky='w')
            self.video_rb = RadioButton(right, text='Video', command=self.set_input_video)
            self.video_rb.grid(row=row, column=3, sticky='')
            row+=1

            self.webcam_active = False
            self.input_settings_frame = NormalFrame(right)
            self.input_settings_frame.grid(row=row, column=0, columnspan=4, sticky='nesw')
            for i in range(6):
                self.input_settings_frame.columnconfigure(i, weight=1)
            self.webcam_rb.invoke()
            row+=1

            self.class_table = ClassTable(right)
            self.class_table.grid(row=row, rowspan=2, column=0, columnspan=4, sticky='nesw', ipadx=5)

            right.rowconfigure(row, weight=0)

            self.spreadrows(row)

    def drawTrainFrame(self):
        
        if(self.clearFrame('Train')):
            self.left = NormalFrame(self)
            left = self.left
            left.pack(side='left', anchor='sw')
            Button(left, type='BIG', text='TRAIN').pack(anchor='sw', side='bottom')
            Button(left, type='BIG', text='STOP').pack(anchor='sw', side='bottom')
            self.pad = NormalFrame(self)
            self.pad.pack(side='right', anchor='w', fill='y')
            Label(self.pad, text='').pack(side='right')
            self.right = NormalFrame(self)
            right = self.right
            right.pack(side='right', expand=True, anchor='sw', fill='both')
            right.columnconfigure(3, weight=1)

            row = 0

            Label(right, text='Epochs').grid(row=row, column=0, columnspan=1, sticky='w')
            self.train_epochs = Entry(right, placeholder_text='10')
            self.train_epochs.grid(row=row, column=1, sticky='w')
            Label(right, text='Target Loss').grid(row=row, column=2, columnspan=1, sticky='e')
            self.target_loss = Entry(right, placeholder_text='0')
            self.target_loss.grid(row=row, column=3, sticky='w')
            row+=1
            
            Label(right, text='Test Split').grid(row=row, column=0, columnspan=1, sticky='w')
            self.test_split_label = Label(right, text='')
            self.test_split_label.grid(row=row, column=3, columnspan=1, sticky='e')
            self.test_split = Slider(right, from_=0, to=100, number_of_steps=400, command=self.test_split_callback)
            self.test_split.grid(row=row, column=1, columnspan=3, sticky = 'w')
            self.test_split.set(15)
            self.test_split_callback(15)

            row+=1

            self.use_cuda = CheckBox(right, text='CUDA')
            self.use_cuda.grid(row=row, column=1, columnspan=1, sticky='w')
            self.use_regularization = CheckBox(right, text='Pose')
            self.use_regularization.grid(row=row, column=3, columnspan=1, sticky='w')
            row+=1

            self.logs_frame = LogFrame(right)
            self.logs_frame.grid(row=row, rowspan=2, column=0, columnspan=4, sticky='nesw')

            right.rowconfigure(row, weight=0)

            self.spreadrows(row)

    def log(self, msg):
        self.logs_frame.update(msg)