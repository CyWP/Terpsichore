from customtkinter import (CTk)
from .tabs import (TabGen,
                   TABS)

class App(CTk):

    def __init__(self):
        super().__init__()

        self.top_tabs = TabGen(master=self,
                               tabs=TABS,
                               orientation='h')
        self.top_tabs.grid(row=0)