from customtkinter import (CTkFrame,
                           CTkLabel)

def drawHelpFrame(master:CTkFrame):
    
    for widget in master.winfo_children():
          widget.destroy()
    CTkLabel(master=master, text='Help').pack()