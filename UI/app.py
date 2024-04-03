from customtkinter import (CTk,
                           CTkFrame,
                           CTkProgressBar,
                           CTkCheckBox,
                           BooleanVar,
                           StringVar,
                           IntVar,
                           DoubleVar)
from .customclasses import Button, Log
from .framedrawer import ConsciousFrame
import asyncio
from taskmanager import TaskManager
from appstate import AppState

class App(CTk):

       def __init__(self):
              super().__init__()
              
              self.title('')
              self.iconbitmap('UI/Assets/dance.ico')
              self.resizable(width=False, height=False)
              self.wm_minsize(width=566, height=328)
              self.title('Load a model')
              self.columnconfigure(0, weight=1)
              self.rowconfigure(0, weight=1)
              self.protocol("WM_DELETE_WINDOW", self.on_closing)

              self.logs = CTkFrame(self, height=0)
              self.logs.pack(anchor='s', side='bottom', fill='x')
              self.log = Log(self.logs, text='v0.0')
              self.log.pack(anchor='e', side='right', fill='x')
              
              self.bottom = CTkFrame(master=self)
              #self.bottom.grid(row=1, column=0, sticky='sew')
              self.bottom.pack(anchor='s', side='bottom', fill='x')

              self.body = ConsciousFrame(master=self)
              #self.body.grid(row=0, column=0, sticky='nesw')
              self.body.pack(anchor='s', fill='both', side='bottom')
              self.rowconfigure(0, weight=1)

              self.body.drawHomeFrame()
              
              title_length = 0.44 # just happens to align with title
              self.bottom.rowconfigure(0, weight=1)
              self.bottom.rowconfigure(1, weight=0)
              for i in range(8):
                     self.bottom.columnconfigure(i, weight=1)

              self.botbar = CTkProgressBar(self.bottom, corner_radius=0, height=4)
              self.botbar.grid(row=1, column=0, columnspan=9, sticky='nesw')
              self.botbar.set(title_length)

              Button(master=self.bottom,
                     text='TERPSICHORE',
                     type='BIG',
                     fct=self.body.drawHomeFrame,
                     frame=self.body,
                     bar=self.botbar,
                     barlevel=title_length).grid(row=0, column=0, columnspan=3, sticky='nsw')
              
              Button(master=self.bottom,
                     text='Perform',
                     type='MENU',
                     fct=self.body.drawMoveFrame,
                     frame=self.body,
                     bar=self.botbar,
                     barlevel=0.59).grid(row=0, column=4, sticky='nesw')
              
              Button(master=self.bottom,
                     text='Record',
                     type='MENU',
                     fct=self.body.drawTraceFrame,
                     frame=self.body,
                     bar=self.botbar,
                     barlevel=0.72).grid(row=0, column=5, sticky='nesw')
              
              Button(master=self.bottom,
                     text='Train',
                     type='MENU',
                     fct=self.body.drawTrainFrame,
                     frame=self.body,
                     bar=self.botbar,
                     barlevel=0.82).grid(row=0, column=6, sticky='nesw')
              
              Button(master=self.bottom,
                     text='',
                     type='IMG',
                     img='UI/Assets/folder.png',
                     fct=AppState.open_folder).grid(row=0, column=7, sticky='nesw')
              
              Button(master=self.bottom,
                     text='',
                     type='IMG',
                     img='UI/Assets/settings.png',
                     fct=AppState.open_github).grid(row=0, column=8, sticky='nesw')
              
             
       async def mainloop(self, *args, **kwargs):
              while True:
                     self.update()
                     await asyncio.sleep(0.01)
       
       async def cancel_all_tasks(self):
              await TaskManager.cancel_tasks()

       def set_ui_inputs(self):
              self.body.set_ui_inputs()
       
       def on_closing(self):
              self.set_ui_inputs()
              AppState.save_ui_state()
              asyncio.create_task(self.cancel_all_tasks())
              self.destroy()
            
       def execute(self, command:str):
              
              self.set_ui_inputs()