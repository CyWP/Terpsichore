from customtkinter import (CTk,
                           FontManager,
                           CTkLabel)
from Panels.tabs import (TabGen,
                        TABS)
from Assets.fonts import FONTS

class App(CTk):

    def __init__(self):
        super().__init__()

        #Load fonts
        for font in FONTS:
            FontManager.load_font(FONTS[font]['path'])

        self.top_tabs = TabGen(master=self,
                               tabs=TABS,
                               orientation='h',
                               homebutton={'text': 'TERPSICHORE',
                                           'font': FONTS['h1']['info'],
                                           'span': 3},
                               font=FONTS['h2']['info'])
        self.top_tabs.grid(row=0, column=0)