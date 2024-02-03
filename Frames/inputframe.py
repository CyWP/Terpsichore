from customtkinter import CTkFrame

def drawInputFrame(master:CTkFrame):
    
    for widget in master.winfo_children():
          widget.destroy()