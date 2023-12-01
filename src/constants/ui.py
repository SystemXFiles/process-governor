from typing import Final

from pydantic.fields import FieldInfo

from configuration.rule import Rule

RULE_COLUMNS: dict[str, FieldInfo] = Rule.model_fields
UI_PADDING = 15
ERROR_COLOR = "#e57373"
ERROR_ROW_COLOR = "#ffcdd2"
TOOLTIP_ICON_SIZE = 75
RE_WIN_SIZE = (900, 600)


class ActionEvents:
    ADD: Final[str] = "<<Add>>"
    DELETE: Final[str] = "<<Delete>>"
    UP: Final[str] = "<<Up>>"
    DOWN: Final[str] = "<<Down>>"
    SAVE: Final[str] = "<<Save>>"


class RulesListEvents:
    UNSAVED_CHANGES_STATE: Final[str] = "<<UnsavedChangesState>>"


class EditableTreeviewEvents:
    CHANGE: Final[str] = "<<Change>>"
    ESCAPE: Final[str] = "<<Escape>>"
    START_EDIT_CELL: Final[str] = "<<StartEditCell>>"

    _SAVE_CELL: Final[str] = "<<SaveCell>>"


class ScrollableTreeviewEvents:
    SCROLL: Final[str] = "<<Scroll>>"
