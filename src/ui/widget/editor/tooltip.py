import tkinter as tk
from tkinter import ttk, StringVar

from tkfontawesome import icon_to_image

from constants.ui import UI_PADDING, ERROR_COLOR, TOOLTIP_ICON_SIZE
from ui.widget.common.label import RichLabel, Image


class Tooltip(ttk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        text = kwargs.pop("text", "")

        super().__init__(master, *args, **kwargs)
        self._text = StringVar(self, value=text)
        self._info_icon = icon_to_image("info-circle", fill="cornflowerblue", scale_to_width=TOOLTIP_ICON_SIZE)
        self._error_icon = icon_to_image("exclamation-triangle", fill=ERROR_COLOR, scale_to_width=TOOLTIP_ICON_SIZE)

        self._image = Image(
            self,
            image=self._info_icon
        )
        self._image.pack(side=tk.LEFT, fill=tk.Y, padx=(0, UI_PADDING))

        label = RichLabel(self, height=4.25, textvariable=self._text)
        label.pack(expand=True, fill=tk.BOTH)
        label.pack_propagate(False)

    def set(self, text: str, error: bool = False):
        if error:
            self._image.configure(image=self._error_icon)
        else:
            self._image.configure(image=self._info_icon)
        self._text.set(text)
