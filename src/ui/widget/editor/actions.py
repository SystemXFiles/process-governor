import tkinter as tk
from tkinter import ttk

from constants.ui import UI_PADDING, ActionEvents
from ui.widget.common.button import IconedButton
from util.ui import icon16px


class ActionsFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setup_btn()

    def _setup_btn(self):
        self.add = add = IconedButton(
            self,
            text=" Add",
            command=lambda: self.event_generate(ActionEvents.ADD),
            image=icon16px("plus", fill="green")
        )

        self.delete = delete = IconedButton(
            self,
            text=" Delete",
            command=lambda: self.event_generate(ActionEvents.DELETE),
            image=icon16px("trash-alt", fill="red")
        )

        self.move_up = move_up = IconedButton(
            self,
            text=" Up",
            command=lambda: self.event_generate(ActionEvents.UP),
            image=icon16px("arrow-up", fill="#1a1a1a")
        )

        self.move_down = move_down = IconedButton(
            self,
            text=" Down",
            command=lambda: self.event_generate(ActionEvents.DOWN),
            image=icon16px("arrow-down", fill="#1a1a1a")
        )

        self.save = save = IconedButton(
            self,
            text=" Save",
            command=lambda: self.event_generate(ActionEvents.SAVE),
            image=icon16px("check", fill="cornflowerblue")
        )

        left_btn_pack = dict(side=tk.LEFT, padx=(0, UI_PADDING))
        add.pack(**left_btn_pack)
        delete.pack(**left_btn_pack)
        move_up.pack(**left_btn_pack)
        move_down.pack(**left_btn_pack)
        save.pack(side=tk.RIGHT)
