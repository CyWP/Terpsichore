from customtkinter import CTkFrame

def drawPlayFrame(master:CTkFrame):
    
    for widget in master.winfo_children():
          widget.destroy()