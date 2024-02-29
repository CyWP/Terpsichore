import os
import random
from customtkinter import get_appearance_mode

FONTS = {
    'h1':
    {
        'path': os.path.abspath('Assets/AlteHaasGroteskBold.ttf'),
        'info': ('Alte Haas Grotesk Bold', 32)
    },
    'h2':
    {
        'path': os.path.abspath('Assets/PPNeueMontreal-Medium.otf'),
        'info': ('PP Neue Montreal Medium', 18)
    },
    'p':
    {
        'path': os.path.abspath('Assets/PPNeueMontreal-Book.otf'),
        'info': ('PP Neue Montreal Medium', 14)
    },
    'tab':
    {
        'path': os.path.abspath('Assets/PPNeueMontreal-Medium.otf'),
        'info': ('PP Neue Montreal Medium', 12)
    }
    }

THEME = {
    'text_hover': '#5000ff',
    'hover_colors': (('#5000ff','#5000ff'),
                     ('#e525b9', '#e525b9'),
                     ('#56c67d', '#56c67d')),
    'widget_padding_x': 20,
    'widget_padding_y': 5
}

def getRandomHoverColor(last_color=''):
    color = THEME['hover_colors'][random.randint(0, len(THEME['hover_colors'])-1)]
    while color == last_color:
        color = THEME['hover_colors'][random.randint(0, len(THEME['hover_colors'])-1)]
    return color

BUTTON_TYPES = {
                'BIG': { 'font': FONTS['h1']['info'],
                         'width': 0,
                         'height': 0,
                         'pad': 4,
                         'border_width': None},
                'MENU': {'font': FONTS['h2']['info'],
                         'width': 0,
                         'height': 0,
                         'pad': 4,
                         'border_width': None},
                'TAB': { 'font': FONTS['tab']['info'],
                         'width': 0,
                         'height': 0,
                         'pad': 3,
                         'border_width': None},
                'IMG': { 'font': FONTS['tab']['info'],
                         'width': 0,
                         'height': 0,
                         'pad': 10,
                         'border_width': None},
                'ACTION': { 'font': FONTS['tab']['info'],
                         'width': 0,
                         'height': 18,
                         'pad': 3,
                         'border_width': 1}      
                }