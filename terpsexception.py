from customtkinter import CTkToplevel, CTkLabel, CTkButton, CTkImage

max_width = 40


class TerpsException(Exception):

    def __init__(self, e):

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

        for line in msg:
            CTkLabel(popup, text=line, padx=20, pady=10).pack()
        CTkButton(popup, text="OK", command=popup.destroy, border_width=2).pack()
        popup.mainloop()
