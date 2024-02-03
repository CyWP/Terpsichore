from customtkinter import (CTk,
                           CTkFrame,
                           CTkProgressBar)
from .customclasses import Button
from .data import (DRAW_FRAME,
                  TABS)

class App(CTk):

    def __init__(self):
        super().__init__()

        self.title('')
        self.iconbitmap('UI/Assets/dance.ico')
        self.wm_minsize(width=400, height=200)

        self.top = CTkFrame(master=self, height=0)
        self.top.grid(row=0, column=0, sticky='new')
        
        self.body = CTkFrame(master=self, height=100)
        self.body.grid(row=1, column=0, sticky='nesw')
        self.rowconfigure(1, weight=1)

        DRAW_FRAME['Home'](self.body)
        
        title_length = 0.348 # just happens to align with title
        self.bottom = CTkFrame(master=self)
        self.bottom.grid(row=2, column=0, sticky='sew')

        self.botbar = CTkProgressBar(self.bottom, corner_radius=0, height=4)
        self.botbar.pack(side='bottom', fill='both')
        self.botbar.set(title_length)

        Button(master=self.bottom,
                   text='TERPSICHORE',
                   type='BIG',
                   fct=DRAW_FRAME['Home'],
                   frame=self.body,
                   bar=self.botbar,
                   barlevel=title_length).pack(side='left', expand=True, fill='both', anchor='w')
        
        for i, tabname in enumerate(TABS):
            Button(master=self.bottom,
                   text=tabname,
                   type='MENU',
                   fct=DRAW_FRAME[tabname],
                   frame=self.body,
                   bar=self.botbar,
                   barlevel=(1-title_length)*(i+1)/(len(TABS)+2)+title_length+0.02).pack(side='left', expand=True, fill='both')
            
        Button(master=self.bottom,
               text='',
               type='IMG',
               img='UI/Assets/settings.png').pack(side='right')
        
        Button(master=self.bottom,
               text='',
               type='IMG',
               img='UI/Assets/folder.png').pack(side='right')