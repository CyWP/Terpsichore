from customtkinter import(FontManager,
                          set_default_color_theme,
                          set_appearance_mode)
from Assets.theme_extras import (THEME,
                                 FONTS)

def load():
    set_default_color_theme('Assets/theme.json')
    set_appearance_mode('light')
    load_fonts()

def load_fonts():
    for font in FONTS:
        FontManager.load_font(FONTS[font]['path'])