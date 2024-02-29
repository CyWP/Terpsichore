from customtkinter import (CTk,
                           CTkFrame,
                           CTkProgressBar,
                           CTkCheckBox,
                           BooleanVar,
                           StringVar,
                           IntVar,
                           DoubleVar)
from .customclasses import Button
#from .data import (DRAW_FRAME,
#                  TABS)
from .framedrawer import ConsciousFrame
import asyncio
from taskmanager import TaskManager

class App(CTk):

       def __init__(self):
              super().__init__()
              
              self.title('')
              self.iconbitmap('UI/Assets/dance.ico')
              self.wm_minsize(width=540, height=300)
              self.columnconfigure(0, weight=1)
              self.protocol("WM_DELETE_WINDOW", self.on_closing)

              #self.load_props()

              self.top = CTkFrame(master=self, height=0)
              self.top.grid(row=0, column=0, sticky='new')
              
              self.body = ConsciousFrame(master=self)
              self.body.grid(row=1, column=0, sticky='nesw')
              self.rowconfigure(1, weight=1)

              self.body.drawHomeFrame()
              
              title_length = 0.45 # just happens to align with title
              self.bottom = CTkFrame(master=self)
              self.bottom.grid(row=2, column=0, sticky='sew')
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
                     barlevel=0.6).grid(row=0, column=4, sticky='nesw')
              
              Button(master=self.bottom,
                     text='Record',
                     type='MENU',
                     fct=self.body.drawTraceFrame,
                     frame=self.body,
                     bar=self.botbar,
                     barlevel=0.725).grid(row=0, column=5, sticky='nesw')
              
              Button(master=self.bottom,
                     text='Train',
                     type='MENU',
                     fct=self.body.drawTrainFrame,
                     frame=self.body,
                     bar=self.botbar,
                     barlevel=0.825).grid(row=0, column=6, sticky='nesw')
              
              Button(master=self.bottom,
                     text='',
                     type='IMG',
                     img='UI/Assets/settings.png').grid(row=0, column=7, sticky='nesw')
              
              '''Button(master=self.bottom,
                     text='',
                     type='IMG',
                     img='UI/Assets/folder.png').grid(row=0, column=8, sticky='nesw')'''
             
       async def mainloop(self, *args, **kwargs):
              while True:
                     self.update()
                     await asyncio.sleep(0.01)
       
       async def cancel_all_tasks(self):
              await TaskManager.cancel_tasks()
       
       def on_closing(self):
              asyncio.create_task(self.cancel_all_tasks())
              self.destroy()
            
       def init_props(self):

              self.show_video = BooleanVar(self, True)

       def w_show_video(self):
              return CTkCheckBox(self, text="Show Video", variable=self.show_video, command= lambda e: self.show_video.set(not self.show_video.get()))