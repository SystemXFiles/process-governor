import tkinter
from tkinter import font, Widget
from tkinter.ttk import Treeview

from tkfontawesome import icon_to_image


def state(widget: Widget) -> str:
    return str(widget["state"])


def full_visible_bbox(tree: Treeview, row_id: str, column_id: str):
    bbox = tree.bbox(row_id, column_id)

    if bbox:
        x, y, width, height = bbox
        y_bottom = y + height
        tree_height = tree.winfo_height()

        if y_bottom <= tree_height:
            return bbox

    return None


def get_parent_with_bg(widget: Widget):
    while widget:
        cfg = widget.configure()

        if cfg and "bg" in cfg:
            return widget

        widget = widget.master
    return None


def get_label_font():
    temp_label = tkinter.Label()
    default_font = font.nametofont(temp_label.cget("font"))
    temp_label.destroy()

    return default_font


def icon16px(name: str, fill: str = None):
    return icon_to_image(name, fill=fill, scale_to_width=16)
