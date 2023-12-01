import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk
from typing import Optional, Literal, List

from constants.ui import EditableTreeviewEvents, ScrollableTreeviewEvents
from ui.widget.common.treeview.scrollable import ScrollableTreeview
from util.ui import full_visible_bbox

ColumnType = Literal["text", "list"]


@dataclass
class CellInfo:
    column_id: str
    row_id: str
    column_name: str
    value: str
    values: List[str]
    type: ColumnType


class CellEditor(ttk.Frame):
    def __init__(
            self,
            master,
            cell_info: CellInfo,
            *args,
            **kwargs
    ):
        super().__init__(master, *args, **kwargs)

        self.cell = cell_info
        self.input = self._setup_widgets()

    def _setup_widgets(self):
        def on_change(_):
            self.event_generate(EditableTreeviewEvents._SAVE_CELL)

        def on_escape(_):
            self.event_generate(EditableTreeviewEvents.ESCAPE)

        if self.cell.type == "text":
            entry_popup = ttk.Entry(self, justify='center')
            entry_popup.insert(0, self.cell.value)
            entry_popup.bind("<FocusOut>", on_change, '+')
        else:
            entry_popup = ttk.Combobox(self, values=self.cell.values, justify='center', state="readonly")
            entry_popup.set(self.cell.value)
            entry_popup.bind("<<ComboboxSelected>>", on_change, '+')

        entry_popup.bind("<Return>", on_change, '+')
        entry_popup.bind("<Escape>", on_escape, '+')
        entry_popup.pack(fill=tk.BOTH)
        entry_popup.focus_force()

        return entry_popup

    def get(self):
        return self.input.get()


class EditableTreeview(ScrollableTreeview):
    _types: dict[str, ColumnType] = {}
    _values: dict[str, List[str]] = {}
    _popup: Optional[CellEditor] = None
    _cell: Optional[CellInfo] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bind("<Button-1>", self._save_and_destroy_popup, '+')
        self.bind("<Double-1>", self._on_dbl_click, '+')
        self.bind(ScrollableTreeviewEvents.SCROLL, self._place_popup, '+')
        self.bind("<Configure>", lambda _: self.after(1, self._place_popup), '+')

    def insert(self, parent, index, iid=None, **kw):
        result = super().insert(parent, index, iid, **kw)
        self.event_generate(EditableTreeviewEvents.CHANGE)
        return result

    def delete(self, *args):
        result = super().delete(*args)
        self.event_generate(EditableTreeviewEvents.CHANGE)
        return result

    def set(self, item, column=None, value=None):
        result = super().set(item, column, value)

        if value is not None:
            self.event_generate(EditableTreeviewEvents.CHANGE)

        return result

    def move(self, item, parent, index):
        result = super().move(item, parent, index)
        self.event_generate(EditableTreeviewEvents.CHANGE)
        return result

    def column_type(self, column: str, ctype: ColumnType):
        self._types[column] = ctype

    def column_values(self, column: str, values: List[str]):
        self._values[column] = values

    def get_cell_info(self, event):
        row_id, column_id = self.identify_row(event.y), self.identify_column(event.x)
        return self._get_cell_info(row_id, column_id)

    def _get_cell_info(self, row_id, column_id):
        if not row_id or not column_id or column_id == "#0":
            return None

        column_name = self.column(column_id)["id"]
        cell_value = self.set(row_id, column_id)
        values = self._values.get(column_name, [])
        cell_type = self._types.get(column_name, "text")

        return CellInfo(
            column_id,
            row_id,
            column_name,
            cell_value,
            values,
            cell_type
        )

    def is_editing(self):
        return self._popup is not None

    def popup(self):
        return self._popup

    def _on_dbl_click(self, event):
        self._destroy_popup()
        self._cell = self.get_cell_info(event)
        self._create_editor()

    def _create_editor(self):
        if not self._cell:
            return

        self._popup = entry_popup = CellEditor(self, self._cell)

        entry_popup.bind(EditableTreeviewEvents._SAVE_CELL, self._save_and_destroy_popup, '+')
        entry_popup.bind(EditableTreeviewEvents.ESCAPE, self._destroy_popup, '+')
        entry_popup.bind("<Destroy>", self._on_popup_destroy, '+')

        self._place_popup()
        self.event_generate(EditableTreeviewEvents.START_EDIT_CELL)

    def _place_popup(self, _=None):
        if not self._popup:
            return

        bbox = full_visible_bbox(self, self._cell.row_id, self._cell.column_id)

        if bbox:
            x, y, width, height = bbox
            self._popup.place(x=x, y=y, width=width, height=height)
        else:
            self._popup.place_forget()

    def _save_and_destroy_popup(self, _=None):
        if self._popup:
            self._save_cell_changes()
            self._destroy_popup()

    def _destroy_popup(self, _=None):
        if self._popup:
            self._popup.destroy()

    def _save_cell_changes(self):
        new_value = self._popup.get().strip()

        if self._cell.value != new_value:
            self.set(self._cell.row_id, self._cell.column_id, new_value)

    def _on_popup_destroy(self, _=None):
        self._popup = None
        self._cell = None

    def edit_cell(self, row_id, column_id):
        self._destroy_popup()
        self._cell = self._get_cell_info(row_id, column_id)
        self._create_editor()
