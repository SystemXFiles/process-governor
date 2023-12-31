import os
import tkinter as tk
from threading import Thread
from tkinter import ttk, messagebox

from constants.any import LOG, LOG_FILE_NAME
from constants.app_info import APP_NAME_WITH_VERSION, APP_NAME
from constants.resources import APP_ICON
from constants.ui import RULE_COLUMNS, UI_PADDING, RC_WIN_SIZE, ActionEvents, RulesListEvents, EditableTreeviewEvents, \
    RC_TITLE
from ui.widget.editor.actions import ActionsFrame
from ui.widget.editor.rules_list import RulesList
from ui.widget.editor.tooltip import Tooltip
from util.messages import yesno_error_box


class RuleConfigurator(tk.Tk):
    _DEFAULT_TOOLTIP = (
        "To add a new rule, click the **Add** button.\n"
        "To edit a rule, **double-click** on the corresponding cell."
    )

    _tree = None
    _tooltip = None
    _actions = None

    def __init__(self):
        super().__init__()
        self._setup_window()
        self._create_widgets()

    def _setup_window(self):
        self._center_window()

        self.protocol("WM_DELETE_WINDOW", self._on_window_closing)
        self.iconbitmap(APP_ICON)
        self.title(f"{RC_TITLE} - {APP_NAME_WITH_VERSION}")
        self.minsize(*RC_WIN_SIZE)

        self.bind_all("<Key>", self._on_key_release, "+")

    @staticmethod
    def _on_key_release(event):
        ctrl = (event.state & 0x4) != 0

        if event.keycode == ord('X') and ctrl and event.keysym.lower() != "x":
            event.widget.event_generate("<<Cut>>")

        if event.keycode == ord('V') and ctrl and event.keysym.lower() != "v":
            event.widget.event_generate("<<Paste>>")

        if event.keycode == ord('C') and ctrl and event.keysym.lower() != "c":
            event.widget.event_generate("<<Copy>>")

        if event.keycode == ord('A') and ctrl and event.keysym.lower() != "c":
            event.widget.event_generate("<<SelectAll>>")

    def _center_window(self):
        x = (self.winfo_screenwidth() // 2) - (RC_WIN_SIZE[0] // 2)
        y = (self.winfo_screenheight() // 2) - (RC_WIN_SIZE[1] // 2)

        self.geometry(f"{RC_WIN_SIZE[0]}x{RC_WIN_SIZE[1]}+{x}+{y}")

    def _create_widgets(self):
        self._create_tooltips()
        self._create_treeview()
        self._create_buttons()

    def _create_tooltips(self):
        self._tooltip = Tooltip(self, text="")
        self._tooltip.pack(fill=tk.X, expand=False, side=tk.TOP, padx=UI_PADDING, pady=(UI_PADDING, 0))

        self._tooltip.set(self._DEFAULT_TOOLTIP)

    def _set_tooltip_by_tree(self, event):
        if not event or not isinstance(event.widget, ttk.Treeview):
            return

        cell = self._tree.get_cell_info(event)

        if cell:
            self._tooltip.set(RULE_COLUMNS[cell.column_name].description)

    def _setup_tooltip(self, widget, text: str, error: bool = False, leave: bool = True, enter: bool = True):
        if enter:
            def on_enter(_):
                self._tooltip.set(text, error)

            widget.bind("<Enter>", on_enter)

        if leave:
            def on_leave(_):
                self._tooltip.set(self._DEFAULT_TOOLTIP)

            widget.bind("<Leave>", on_leave)

    def _setup_tooltip_cell_editor(self, _=None):
        cell = self._tree.current_cell()

        if cell:
            self._setup_tooltip(
                self._tree.popup(),
                RULE_COLUMNS[cell.column_name].description,
                leave=False
            )

    def _create_treeview(self):
        self._tree = tree = RulesList(self)

        tree.bind("<<TreeviewSelect>>", self._update_buttons_state, "+")
        tree.bind("<Control-Key>", self._on_key_press_tree, "+")
        tree.bind("<Delete>", self._delete_selected, "+")
        tree.bind("<Motion>", self._set_tooltip_by_tree, "+")
        tree.bind(RulesListEvents.UNSAVED_CHANGES_STATE, self._update_buttons_state, "+")
        tree.bind(EditableTreeviewEvents.START_EDIT_CELL, self._setup_tooltip_cell_editor, "+")

        tree.pack(fill=tk.BOTH, expand=True, padx=UI_PADDING, pady=UI_PADDING)

        tree.error_icon_created = lambda icon, tooltip: self._setup_tooltip(icon, tooltip, True, False)

        self._setup_tooltip(tree, "", enter=False)

    def _on_key_press_tree(self, event):
        ctrl = (event.state & 0x4) != 0

        if ctrl and event.keycode == ord('A'):
            self._select_all(event)

    def _create_buttons(self):
        self._actions = actions = ActionsFrame(self)
        actions.pack(fill=tk.X, padx=UI_PADDING, pady=(0, UI_PADDING))
        actions.bind(ActionEvents.ADD, lambda _: self._add(), "+")
        actions.bind(ActionEvents.DELETE, lambda _: self._delete_selected(), "+")
        actions.bind(ActionEvents.UP, lambda _: self._move_item_up(), "+")
        actions.bind(ActionEvents.DOWN, lambda _: self._move_item_down(), "+")
        actions.bind(ActionEvents.SAVE, lambda _: self._save(), "+")

        self._setup_tooltip(actions.add, "__Adds__ a rule after the current")
        self._setup_tooltip(actions.delete, "__Deletes__ the selected rules")
        self._setup_tooltip(actions.move_up, "__Moves__ the current rule __up__")
        self._setup_tooltip(actions.move_down, "__Moves__ the current rule __down__")
        self._setup_tooltip(actions.save, "__Saves__ the settings")

        self._update_buttons_state()

    def _move_item_up(self):
        selected_items = self._tree.selection()

        if selected_items:
            selected_item = selected_items[0]
            index = self._tree.index(selected_item)

            if index > 0:
                self._tree.move(selected_item, '', index - 1)
                self._tree.selection_set(selected_item)
                self._update_buttons_state()

    def _move_item_down(self):
        selected_items = self._tree.selection()

        if selected_items:
            selected_item = selected_items[0]
            index = self._tree.index(selected_item)
            next_index = index + 1

            if next_index < len(self._tree.get_children()):
                self._tree.move(selected_item, '', next_index)
                self._tree.selection_set(selected_item)
                self._update_buttons_state()

    def _save(self):
        if not self._tree.save_data():
            messagebox.showerror(f"Error Detected - {APP_NAME_WITH_VERSION}", "An error occurred while saving.")

    def _add(self):
        selected_items = self._tree.selection()

        if selected_items:
            selected_item = selected_items[0]
            index = self._tree.index(selected_item)

            self._tree.insert('', index + 1)
            self._tree.selection_set(self._tree.get_children()[index + 1])
        else:
            self._tree.insert('', 'end')

        self._update_buttons_state()

    def _delete_selected(self, _=None):
        selected_items = self._tree.selection()

        if selected_items:
            index = self._tree.index(selected_items[0])

            for item in selected_items:
                self._tree.delete(item)

            children = self._tree.get_children()

            if len(children) <= index:
                index -= 1

            if children and len(children) > index:
                self._tree.selection_set(children[index])

        self._update_buttons_state()

    def _select_all(self, _):
        items = self._tree.get_children()

        if items:
            self._tree.selection_set(items)
            self._update_buttons_state()

    def _on_window_closing(self):
        if self._tree.unsaved_changes:
            if self._tree.has_error():
                message = "There are unsaved changes. Do you want to discard them and exit?"
                result = messagebox.askyesno(f"{RC_TITLE} - {APP_NAME_WITH_VERSION}", message)

                if not result:
                    return
            else:
                message = "There are unsaved changes. Do you want to save them before exiting?"
                result = messagebox.askyesnocancel(f"{RC_TITLE} - {APP_NAME_WITH_VERSION}", message)

                if result is None:
                    return

                if result and not self._tree.save_data():
                    messagebox.showerror(f"Error Detected - {APP_NAME_WITH_VERSION}", "An error occurred while saving.")
                    return

        self.destroy()

    def _update_buttons_state(self, _=None):
        tree = self._tree
        actions = self._actions
        selected_items = tree.selection()

        if selected_items:
            selected_item = selected_items[0]
            index = tree.index(selected_item)
            total_items = len(tree.get_children())

            actions.move_up["state"] = tk.NORMAL if index > 0 else tk.DISABLED
            actions.move_down["state"] = tk.NORMAL if index < total_items - 1 else tk.DISABLED
        else:
            actions.move_up["state"] = tk.DISABLED
            actions.move_down["state"] = tk.DISABLED

        actions.save["state"] = tk.NORMAL if tree.unsaved_changes and not tree.has_error() else tk.DISABLED
        actions.delete["state"] = tk.NORMAL if selected_items else tk.DISABLED


is_editor_open = False


def open_rule_editor():
    global is_editor_open

    def editor():
        global is_editor_open
        try:
            is_editor_open = True

            app = RuleConfigurator()
            app.mainloop()
        except:
            LOG.exception(f"An unexpected error occurred in the {RC_TITLE} of {APP_NAME}.")
            show_rule_editor_error_message()
        finally:
            is_editor_open = False

    if not is_editor_open:
        thread = Thread(target=editor)
        thread.start()


def show_rule_editor_error_message():
    title = f"Error Detected - {APP_NAME_WITH_VERSION}"
    message = (
        f"An error has occurred in the {RC_TITLE} of {APP_NAME}.\n"
        f"To troubleshoot, please check the log file `{LOG_FILE_NAME}` for details.\n\n"
        f"Would you like to open the log file?"
    )

    if yesno_error_box(title, message):
        os.startfile(LOG_FILE_NAME)


if __name__ == "__main__":
    test_app = RuleConfigurator()
    test_app.mainloop()
