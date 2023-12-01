import tkinter as tk
from tkinter import ttk

from constants.ui import ScrollableTreeviewEvents


class ScrollableTreeview(ttk.Treeview):
    def __init__(self, master=None, *args, **kwargs):
        self._frame = ttk.Frame(master)
        self._scrollbar = ttk.Scrollbar(
            self._frame,
            orient="vertical"
        )

        super().__init__(self._frame, *args, **kwargs)

        self._scrollbar.configure(command=self._on_scrollbar)
        super().configure(yscrollcommand=self._on_scrollbar_mouse)

        self._scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        super().pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

    def on_scroll(self):
        pass

    def pack_configure(self, *args, **kwargs):
        self._frame.pack_configure(*args, **kwargs)

    def pack_forget(self):
        self._frame.pack_forget()

    def pack_info(self):
        return self._frame.pack_info()

    def place_configure(self, *args, **kwargs):
        self._frame.place_configure(*args, **kwargs)

    def place_forget(self):
        self._frame.place_forget()

    def place_info(self):
        return self._frame.place_info()

    pack = configure = config = pack_configure
    forget = pack_forget
    info = pack_info

    def _on_scrollbar(self, *args):
        self.yview(*args)
        self.event_generate(ScrollableTreeviewEvents.SCROLL)

    def _on_scrollbar_mouse(self, first, last):
        self._scrollbar.set(first, last)
        self.event_generate(ScrollableTreeviewEvents.SCROLL)
