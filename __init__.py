import customtkinter
from loader import load
from app import App

if __name__ == '__main__':

    load()

    app = App()
     
    app.mainloop()