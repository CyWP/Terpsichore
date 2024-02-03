from customtkinter import CTkFrame

def drawViewFrame(master:CTkFrame):
    
    for widget in master.winfo_children():
          widget.destroy()