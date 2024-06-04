from customtkinter import CTkToplevel, CTkLabel, CTkButton
import traceback
import shutil
from os import path

max_width = 40


class TerpsException(Exception):

    def __init__(self, e):
        try:
            traceback.print_exc(e)
        except:
            pass
        message = str(e)
        msg = []

        while len(message) > max_width:
            msg.append(message[:max_width])
            message = message[max_width:]
        msg.append(message)

        super().__init__(message)

        popup = CTkToplevel()
        # popup.title("Error")
        popup.wm_overrideredirect(1)

        CTkLabel(popup, text="ERROR", padx=20, pady=10).pack()
        for line in msg:
            CTkLabel(popup, text=line, padx=20, pady=10).pack()
        CTkButton(popup, text="OK", command=popup.destroy, border_width=2).pack()
        popup.mainloop()

class InvalidModelException(Exception):

    def __init__(self, e, modelpath):
        try:
            traceback.print_exc(e)
        except:
            pass
        message = str(e)
        msg = []
        self.modelpath = modelpath

        while len(message) > max_width:
            msg.append(message[:max_width])
            message = message[max_width:]
        msg.append(message)

        super().__init__(message)

        popup = CTkToplevel()
        # popup.title("Error")
        popup.wm_overrideredirect(1)
        self.popup = popup

        CTkLabel(popup, text="ERROR", padx=20, pady=10).pack()
        for line in msg:
            CTkLabel(popup, text=line, padx=20, pady=10).pack()
        CTkButton(popup, text="Keep Model", command=popup.destroy, border_width=2).pack()
        CTkButton(popup, text="Delete Model", command=self.delete, border_width=2).pack()
        popup.mainloop()

    def delete(self):
        try:
            shutil.rmtree(path.abspath(self.modelpath))
            self.popup.destroy()
        except:
            pass