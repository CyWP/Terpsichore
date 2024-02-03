from customtkinter import (CTkButton,
                           CTkImage,
                           get_appearance_mode)
from PIL import Image
import matplotlib.colors as colors
import numpy as np
from Assets.theme_extras import (THEME,
                                 BUTTON_TYPES,
                                 getRandomHoverColor)

class Button(CTkButton):

    def click(self, color):
         self.colorButton(color)
         if self.bar is not None:             
            self.bar.configure(progress_color=color)
            self.bar.set(self.barlevel)

    def colorButton(self, color):
            self.last_color = color
            if self.img is not None:
                self.configure(image=colorize(self.img, color))
            else:
                self.configure(text_color=color)

    def __init__(self, master, type, img=None, bar=None, barlevel=0., **kwargs):

        super().__init__(master,
                         font=BUTTON_TYPES[type]['font'],
                         width=BUTTON_TYPES[type]['width'],
                         height=BUTTON_TYPES[type]['height'],
                         border_spacing=BUTTON_TYPES[type]['pad'],
                         **kwargs)
        
        self.bar = bar
        self.barlevel = barlevel

        base_color = self.cget('text_color')

        self.img = img
        if img is not None:
            self.colorButton(base_color)

        self.bind('<Enter>', lambda event: self.colorButton(getRandomHoverColor()))
        self.bind('<Leave>', lambda event: self.colorButton(base_color))
        self.bind('<Button-1>', lambda event: self.click(getRandomHoverColor(self.last_color)))

def hex_to_rgb(value):
    return tuple([int(255*x) for x in colors.hex2color(value)])

def colorize(filename, color):
    color = color[get_appearance_mode=='dark']
    replacement_color = hex_to_rgb(color)
    img = Image.open(filename)
    r, g, b, a = img.split()
    r = r.point(lambda i: replacement_color[0])
    g = g.point(lambda i: replacement_color[1])
    b = b.point(lambda i: replacement_color[2])
    img = Image.merge('RGBA', (r, g, b, a))
    return CTkImage(light_image=img, dark_image=img)