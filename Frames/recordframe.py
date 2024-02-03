from customtkinter import CTkFrame

def drawRecordFrame(master:CTkFrame):
    
    for widget in master.winfo_children():
          widget.destroy()