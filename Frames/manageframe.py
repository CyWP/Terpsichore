from customtkinter import CTkFrame

def drawManageFrame(master:CTkFrame):
    
    for widget in master.winfo_children():
          widget.destroy()