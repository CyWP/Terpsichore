from customtkinter import (CTkButton,
                           CTkFrame,
                           CTkImage,
                           CTkCheckBox,
                           CTkLabel,
                           CTkComboBox,
                           CTkRadioButton,
                           CTkEntry,
                           get_appearance_mode)
from PIL import Image
import matplotlib.colors as colors
import numpy as np
from .Assets import (BUTTON_TYPES,
                     THEME,
                     FONTS,
                     getRandomHoverColor)


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
class Button(CTkButton):

    def click(self, color):
         self.fct()
         self.colorButton(color)
         if self.bar is not None:             
            self.bar.configure(progress_color=color)
            self.bar.set(self.barlevel)

    def colorButton(self, color):
            self.last_color = color
            if self.img is not None:
                self.configure(image=colorize(self.img, color))
            else:
                self.configure(text_color=color, border_color=color)

    def __init__(self,
                 master,
                 type,
                 fct= lambda e: None,
                 frame=None,
                 img=None,
                 bar=None,
                 barlevel=0.,
                 **kwargs):

        super().__init__(master,
                         font=BUTTON_TYPES[type]['font'],
                         width=BUTTON_TYPES[type]['width'],
                         height=BUTTON_TYPES[type]['height'],
                         border_spacing=BUTTON_TYPES[type]['pad'],
                         border_width=BUTTON_TYPES[type]['border_width'],
                         **kwargs)
        
        self.frame = frame
        self.fct = fct
        self.bar = bar
        self.barlevel = barlevel

        base_color = self.cget('text_color')

        self.img = img
        if img is not None:
            self.colorButton(base_color)

        self.bind('<Enter>', lambda event: self.colorButton(getRandomHoverColor()))
        self.bind('<Leave>', lambda event: self.colorButton(base_color))
        self.bind('<Button-1>', lambda event: self.click(getRandomHoverColor(self.last_color)))
    
class NormalFrame(CTkFrame):

    def __init__(self, args, **kwargs):

        super().__init__(args, **kwargs)

class Label(CTkLabel):

    def __init__(self, args, **kwargs):

        super().__init__(args, font=FONTS['p']['info'], **kwargs)

    def grid(self, **kwargs):

        super().grid(ipadx=THEME['widget_padding_x'],
                     ipady=THEME['widget_padding_y'],
                     **kwargs)
        
class ComboBox(CTkComboBox):

    def __init__(self, args, **kwargs):
        
        super().__init__(args, font=FONTS['tab']['info'], dropdown_font=FONTS['tab']['info'], justify='center', state='readonly', **kwargs)

        self.base_color = self.cget('text_color')

        self.bind('<Leave>', lambda event: self.colorButton(self.base_color))
        self.bind('<Enter>', lambda event: self.colorButton(getRandomHoverColor()))
        self.bind('<Button-1>', lambda event: self.click(getRandomHoverColor()))

        self.set(self.cget('values')[0])

    def click(self, color):
         self.colorButton(color)
         self.configure(dropdown_hover_color=color)

    def colorButton(self, color):
            self.configure(button_hover_color=color, text_color=color)

class CheckBox(CTkCheckBox):

    def __init__(self, args, **kwargs):
        
        super().__init__(args, font=FONTS['p']['info'], checkbox_height=14, checkbox_width=14, **kwargs)
        self.base_color = self.cget('border_color')

        self.bind('<Leave>', lambda event: self.configure(border_color=self.base_color, checkmark_color=self.base_color))
        self.bind('<Enter>', lambda event: self.configure(border_color=getRandomHoverColor(), checkmark_color=getRandomHoverColor()))
        self.bind('<Button-1>', lambda event: self.configure(checkmark_color=getRandomHoverColor()))

class RadioButton(CTkRadioButton):

    def __init__(self, args, **kwargs):
        
        super().__init__(args, radiobutton_height=14, radiobutton_width=14, font=FONTS['p']['info'], **kwargs)

        self.base_color = self.cget('text_color')

        self.bind('<Leave>', lambda event: self.colorButton(self.base_color))
        self.bind('<Enter>', lambda event: self.colorButton(getRandomHoverColor()))
        self.bind('<Button-1>', lambda event: self.click(getRandomHoverColor()))

    def invoke(self, event: int=0):
         super().invoke(event)
         self.click(getRandomHoverColor())

    def click(self, color):
        self.colorButton(color)

    def colorButton(self, color):
            self.configure(fg_color=color, hover_color=color)

    def deactivate(self):
         self.deselect()
         self.colorButton(self.base_color)

class Entry(CTkEntry):
     
     def __init__(self, args, **kwargs):
          
          super().__init__(args, height=18, font=FONTS['tab']['info'], **kwargs)