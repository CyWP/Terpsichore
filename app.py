from tkinter import PhotoImage
from customtkinter import (CTk,
                           CTkFrame,
                           FontManager,
                           CTkLabel,
                           CTkButton,
                           CTkProgressBar,
                           CTkImage)
from tabs import (TabGen)
from button import Button
from groups import(TABS,
                   BOTTOM_BUTTONS)
from Frames.homeframe import drawHomeFrame
from Assets.theme_extras import(THEME,
                                FONTS)
from windowbar import TitleBar

class App(CTk):

    def __init__(self):
        super().__init__()

        #self.wm_attributes('-toolwindow', 'True')
        self.title('')
        self.iconbitmap('Assets/dance.ico')

        #TitleBar(parent=self, bg=self.cget('fg_color')).pack(fill='both')

        self.top = CTkFrame(master=self)
        self.top.pack(fill='both')
        
        self.body = CTkFrame(master=self)
        self.body.pack(fill='both')
        drawHomeFrame(master=self.body)
        #self.body.bind('<Motion>', self.overrideredirect(True))
        
        title_length = 0.348
        self.bottom = CTkFrame(master=self)
        self.bottom.pack(side='bottom', fill='both')
        self.botbar = CTkProgressBar(self.bottom, corner_radius=0, height=4)
        self.botbar.pack(side='bottom', fill='both')
        self.botbar.set(title_length)
        Button(master=self.bottom,
                   text='TERPSICHORE',
                   type='BIG',
                   bar=self.botbar,
                   barlevel=title_length).pack(side='left', expand=True, fill='both', anchor='w')
        for i, tabname in enumerate(TABS):
            Button(master=self.bottom,
                   text=tabname,
                   type='MENU',
                   bar=self.botbar,
                   barlevel=(1-title_length)*(i+1)/(len(TABS)+2)+title_length+0.02).pack(side='left', expand=True, fill='both')
        Button(master=self.bottom,
               text='',
               type='IMG',
               img='Assets/settings.png').pack(side='right')
        Button(master=self.bottom,
               text='',
               type='IMG',
               img='Assets/folder.png').pack(side='right')