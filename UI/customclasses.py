from customtkinter import (
    CTkButton,
    CTkFrame,
    CTkImage,
    CTkCheckBox,
    CTkLabel,
    CTkComboBox,
    CTkRadioButton,
    CTkEntry,
    CTkScrollableFrame,
    CTkSlider,
    get_appearance_mode,
)
from PIL import Image
import matplotlib.colors as colors
import numpy as np
from .Assets import BUTTON_TYPES, THEME, FONTS, getRandomHoverColor
from appstate import AppState
import asyncio


def hex_to_rgb(value):
    return tuple([int(255 * x) for x in colors.hex2color(value)])


def colorize(filename, color, size=None):
    color = color[get_appearance_mode == "dark"]
    replacement_color = hex_to_rgb(color)
    img = Image.open(filename)
    r, g, b, a = img.split()
    r = r.point(lambda i: replacement_color[0])
    g = g.point(lambda i: replacement_color[1])
    b = b.point(lambda i: replacement_color[2])
    img = Image.merge("RGBA", (r, g, b, a))
    img = CTkImage(light_image=img, dark_image=img)
    if size is not None:
        img.configure(size=size)
    return img


class ColImage(CTkLabel):

    def __init__(self, master, path, size: tuple, color, anchor="nw"):

        self.path = path
        self.size = size
        img = colorize(path, color, self.size)
        img.configure(size=size)
        super().__init__(master, image=img, text="", anchor=anchor)

        self.bind("<Enter>", lambda event: self.color(getRandomHoverColor()))
        self.bind("<Leave>", lambda event: self.color(color))

    def color(self, color):
        self.configure(image=colorize(self.path, color, self.size))


class Button(CTkButton):

    def click(self, color):
        self.fct()
        self.colorButton(color)
        if self.bar is not None:
            self.bar.configure(progress_color=color)
            self.bar.set(self.barlevel)

    def colorButton(self, color):
        self.last_color = color
        if self.img is not None:
            self.configure(image=colorize(self.img, color))
        else:
            self.configure(text_color=color, border_color=color)

    def __init__(
        self,
        master,
        type,
        fct=lambda: None,
        frame=None,
        img=None,
        size=(64, 64),
        bar=None,
        barlevel=0.0,
        **kwargs,
    ):

        super().__init__(
            master,
            font=BUTTON_TYPES[type]["font"],
            width=BUTTON_TYPES[type]["width"],
            height=BUTTON_TYPES[type]["height"],
            border_spacing=BUTTON_TYPES[type]["pad"],
            border_width=BUTTON_TYPES[type]["border_width"],
            **kwargs,
        )

        self.frame = frame
        self.fct = fct
        self.bar = bar
        self.barlevel = barlevel
        self.size = size

        base_color = self.cget("text_color")

        self.img = img
        if img is not None:
            self.colorButton(base_color)

        self.bind("<Enter>", lambda event: self.colorButton(getRandomHoverColor()))
        self.bind("<Leave>", lambda event: self.colorButton(base_color))
        self.bind(
            "<Button-1>", lambda event: self.click(getRandomHoverColor(self.last_color))
        )


class NormalFrame(CTkFrame):

    def __init__(self, args, **kwargs):

        super().__init__(args, width=0, height=0, **kwargs)

    def grid(self, **kwargs):

        super().grid(ipadx=5, **kwargs)


class Label(CTkLabel):

    def __init__(self, args, anchor="w", **kwargs):

        super().__init__(
            args, font=FONTS["p"]["info"], height=32, anchor=anchor, **kwargs
        )

    def grid(self, **kwargs):

        super().grid(
            ipadx=THEME["widget_padding_x"], ipady=THEME["widget_padding_y"], **kwargs
        )


class Log(CTkLabel):

    def __init__(self, args, **kwargs):

        super().__init__(args, font=FONTS["tab"]["info"], height=18, **kwargs)

    def pack(self, **kwargs):

        super().pack(ipadx=0, ipady=0, padx=0, pady=0, **kwargs)


class ComboBox(CTkComboBox):

    def __init__(self, master, *args, **kwargs):

        self.frame = NormalFrame(master, corner_radius=1, border_width=1,)
        super().__init__(
            self.frame,
            *args,
            font=FONTS["tab"]["info"],
            dropdown_font=FONTS["tab"]["info"],
            justify="center",
            state="readonly",
            **kwargs,
        )
        self.base_color = self.cget("text_color")

        self.bind("<Leave>", lambda event: self.colorButton(self.base_color))
        self.bind("<Enter>", lambda event: self.colorButton(getRandomHoverColor()))
        self.bind("<Button-1>", lambda event: self.click(getRandomHoverColor()))

        self.set(self.cget("values")[0])

    def click(self, color):
        self.colorButton(color)
        self.configure(dropdown_hover_color=color)

    def colorButton(self, color):
        self.configure(button_hover_color=color, text_color=color)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)
        super().grid(sticky="nesw", padx=1, pady=1)

class CheckBox(CTkCheckBox):

    def __init__(self, args, **kwargs):

        super().__init__(
            args,
            font=FONTS["p"]["info"],
            checkbox_height=20,
            checkbox_width=20,
            **kwargs,
        )
        self.base_color = self.cget("border_color")

        self.bind(
            "<Leave>",
            lambda event: self.configure(
                border_color=self.base_color, checkmark_color=self.base_color
            ),
        )
        self.bind(
            "<Enter>",
            lambda event: self.configure(
                border_color=getRandomHoverColor(),
                checkmark_color=getRandomHoverColor(),
            ),
        )
        self.bind(
            "<Button-1>",
            lambda event: self.configure(checkmark_color=getRandomHoverColor()),
        )


class RadioButton(CTkRadioButton):

    def __init__(self, args, **kwargs):

        super().__init__(
            args,
            radiobutton_height=20,
            radiobutton_width=20,
            font=FONTS["p"]["info"],
            **kwargs,
        )

        self.base_color = self.cget("text_color")

        self.bind("<Leave>", lambda event: self.colorButton(self.base_color))
        self.bind("<Enter>", lambda event: self.colorButton(getRandomHoverColor()))
        self.bind("<Button-1>", lambda event: self.click(getRandomHoverColor()))

    def invoke(self, event: int = 0):
        super().invoke(event)
        self.click(getRandomHoverColor())

    def click(self, color):
        self.colorButton(color)

    def colorButton(self, color):
        self.configure(fg_color=color, hover_color=color)

    def deactivate(self):
        self.deselect()
        self.colorButton(self.base_color)


class Entry(CTkEntry):

    def __init__(self, args, width=54, **kwargs):

        super().__init__(
            args, height=32, width=width, font=FONTS["tab"]["info"], **kwargs
        )

    def clear(self):
        self.delete(0, (len(self.get())))


class ClassTable(CTkScrollableFrame):

    def __init__(self, args, **kwargs):

        super().__init__(
            args, corner_radius=1, border_width=1, width=240, height=200, **kwargs
        )
        self._scrollbar._set_dimensions(width=10, height=208)
        for i in range(5):
            self.columnconfigure(i, weight=1)

        self.draw()

    def draw(self):

        for widget in self.winfo_children():
            widget.destroy()

        Log(self, text="Gesture").grid(row=0, column=1, sticky="w")
        Log(self, text="Samples").grid(row=0, column=2, sticky="w")
        Log(self, text="Size").grid(row=0, column=3, sticky="w")

        i = 1
        for name, recs, space in AppState.get_gestures():
            if name == AppState.get_active_gesture():
                Label(self, text=">>>").grid(row=i, column=0, sticky="w")
            else:
                Button(
                    self,
                    type="ACTION",
                    text="Select",
                    command=lambda n=name: self.select_gesture(n),
                ).grid(row=i, column=0, sticky="w", padx=4, ipadx=4, pady=4)
            Log(self, text=name).grid(row=i, column=1, sticky="w")
            Log(self, text=recs).grid(row=i, column=2, sticky="w")
            Log(self, text=space).grid(row=i, column=3, sticky="w")
            Button(
                self,
                type="ACTION",
                text="Delete",
                command=lambda n=name: self.remove_gesture(n),
            ).grid(row=i, column=4, sticky="e", padx=4, ipadx=4)
            i += 1

    def grid(self, **kwargs):
        self.draw()
        super().grid(**kwargs)

    def remove_gesture(self, name):
        AppState.remove_gesture(name)
        self.draw()

    def add_gesture(self, name):
        AppState.new_gesture(name)
        self.draw()

    def select_gesture(self, name):
        AppState.select_gesture(name)
        self.draw()


class LogFrame(CTkScrollableFrame):

    def __init__(self, args, **kwargs):

        super().__init__(
            args, corner_radius=1, border_width=1, width=240, height=250, **kwargs
        )
        self._scrollbar._set_dimensions(width=10, height=328)
        self.max_label_length = 125
        Log(self, text="Training Logs").pack(anchor="w", side="top")

    async def listen(self):
        self.clear()
        while AppState._training:
            for log in AppState.get_train_logs():
                log = str(log)
                while len(log) > self.max_label_length:
                    Log(self, text=log[: self.max_label_length]).pack(
                        anchor="w", side="top"
                    )
                    log = log[self.max_label_length :]
                Log(self, text=log).pack(anchor="w", side="top")
            await asyncio.sleep(0.5)

    def clear(self):
        for child in self.winfo_children()[1:]:
            child.destroy()


class ModelInfoFrame(CTkScrollableFrame):

    def __init__(self, args, **kwargs):
        super().__init__(
            args, corner_radius=1, border_width=1, width=360, height=282, **kwargs
        )
        self._scrollbar._set_dimensions(width=10, height=328)
        self.max_label_length = 24
        self.draw()

    def draw(self):
        for widget in self.winfo_children():
            widget.destroy()
        info = AppState.active_model_info()
        gestures = AppState.get_gestures()
        trained_gestures = AppState.get_trained_info()
        row = 0
        self.columnconfigure(index=(0, 1), weight=1)
        if info is None:
            Log(self, text="Load or Create a model", anchor="center").grid(
                row=row, column=0, columnspan=2, sticky="w"
            )
        else:
            Log(self, text="Current Model", anchor="center").grid(
                row=row, column=0, columnspan=2, sticky="w"
            )
            row += 1
            Log(self, text="", anchor="center").grid(
                row=row, column=0, columnspan=2, sticky="w"
            )
            row += 1
            for name, val in info:
                Log(self, text=self.format(name)).grid(row=row, column=0, sticky="w")
                Log(self, text=self.format(str(val))).grid(
                    row=row, column=1, sticky="e"
                )
                row += 1
            Log(self, text="", anchor="center").grid(
                row=row, column=0, columnspan=2, sticky="w"
            )
            row += 1
            Log(self, text="Current Gestures", anchor="center").grid(
                row=row, column=0, columnspan=2, sticky="w"
            )
            row += 1
            Log(self, text="", anchor="center").grid(
                row=row, column=0, columnspan=2, sticky="w"
            )
            row += 1
            for name, recs, space in gestures:
                Log(
                    self, text=self.format(f"{name}: {recs} samples ({space})", 1.75)
                ).grid(row=row, column=0, columnspan=2, sticky="e")
                row += 1
            Log(self, text="", anchor="center").grid(
                row=row, column=0, columnspan=2, sticky="w"
            )
            row += 1
            Log(self, text="Trained Gestures", anchor="center").grid(
                row=row, column=0, columnspan=2, sticky="w"
            )
            row += 1
            Log(self, text="", anchor="center").grid(
                row=row, column=0, columnspan=2, sticky="w"
            )
            row += 1
            for name, label in trained_gestures:
                Log(
                    self,
                    text=self.format(
                        f"{name}, label: {label} {[1 if i==label else 0 for i in range(len(trained_gestures))]}",
                        1.75,
                    ),
                ).grid(row=row, column=0, columnspan=2, sticky="e")
                row += 1

    def grid(self, **kwargs):
        self.draw()
        super().grid(**kwargs)

    def format(self, text, mult=1.0):
        max = int(mult * self.max_label_length)
        if len(text) > max:
            return f"...{text[-max:]}"
        return text


class LoadModelFrame(CTkScrollableFrame):

    def __init__(self, args, refresh=None, **kwargs):
        super().__init__(
            args, corner_radius=1, border_width=1, width=180, height=254, **kwargs
        )
        self._scrollbar._set_dimensions(width=10, height=370)
        self.refresh = refresh
        self.draw()

    def draw(self):
        for widget in self.winfo_children():
            widget.destroy()

        Log(self, text="Load Model", anchor="w").pack(side="top", fill="x")
        for i, model in enumerate(AppState.get_models()):
            Button(
                self,
                type="ACTION",
                text=model,
                command=lambda n=model: self.load_model(n),
            ).pack(side="top", fill="x", pady=4, padx=(8, 4))

    def grid(self, **kwargs):
        self.draw()
        super().grid(**kwargs)

    def load_model(self, name):
        self.draw()
        AppState.load_model(name)
        if self.refresh is not None:
            self.refresh()

class Slider(CTkSlider):

    def __init__(self, args, **kwargs):

        super().__init__(args, height=3, border_width=1, **kwargs)

        self.bind("<Enter>", lambda event: self.colorButton(getRandomHoverColor()))
        self.bind("<Button-1>", lambda event: self.click(getRandomHoverColor()))

    def click(self, color):
        self.colorButton(color)

    def colorButton(self, color):
        self.configure(button_color=color, progress_color=color)

    def grid(self, padx=(0, 54), **kwargs):
        super().grid(padx=padx, **kwargs)