from customtkinter import (CTkFrame,
                           CTkLabel)
from CTkTable import *

def drawHomeFrame(master:CTkFrame):
    
    for widget in master.winfo_children():
          widget.destroy()
    CTkLabel(master=master, text='Home').pack()