from customtkinter import CTkFrame

def drawTrainFrame(master:CTkFrame):
    
    for widget in master.winfo_children():
          widget.destroy()