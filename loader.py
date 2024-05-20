from customtkinter import FontManager, set_default_color_theme, set_appearance_mode
from UI.Assets import FONTS


def load():
    set_default_color_theme("UI/Assets/theme.json")
    set_appearance_mode("light")
    load_fonts()


def load_fonts():
    for font in FONTS:
        FontManager.load_font(FONTS[font]["path"])


def load_props(master):
    pass
