import re
import tkinter as tk
from tkinter import font
from tkinter.ttk import Label

from util.ui import get_parent_with_bg, get_label_font


class WrappingLabel(tk.Label):
    def __init__(self, master=None, **kwargs):
        tk.Label.__init__(self, master, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()), '+')


class RichLabel(tk.Text):
    def __init__(self, *args, text="", textvariable=None, **kwargs):
        kwargs.setdefault("borderwidth", 0)
        kwargs.setdefault("relief", "flat")
        kwargs.setdefault("highlightthickness", 0)
        kwargs.setdefault("cursor", "arrow")
        kwargs["takefocus"] = False

        super().__init__(*args, **kwargs)
        self._textvariable = textvariable

        if "bg" not in kwargs:
            def _set_bg(event):
                parent = get_parent_with_bg(event.widget)
                if parent:
                    self.configure(bg=parent.cget("bg"))

            self.bind("<Map>", _set_bg, '+')

        default_font = get_label_font()

        self.configure(font=default_font)

        font_configure = default_font.configure()
        bold_font = font.Font(**font_configure)
        italic_font = font.Font(**font_configure)
        underline_font = font.Font(**font_configure)
        overstrike_font = font.Font(**font_configure)
        code_font = self.get_monospace_font(default_font)

        bold_font.configure(weight="bold")
        italic_font.configure(slant="italic")
        underline_font.configure(underline=True)
        overstrike_font.configure(overstrike=True)

        self.tag_configure("bold", font=bold_font)
        self.tag_configure("italic", font=italic_font)
        self.tag_configure("underline", font=underline_font)
        self.tag_configure("overstrike", font=overstrike_font)
        self.tag_configure("code", font=code_font)

        if text:
            self.configure(text=text)

        self.bind("<FocusIn>", lambda e: self.focus_set(), '+')
        self.bind("<1>", lambda event: "break", '+')
        self.bind("<Double-1>", lambda event: "break", '+')
        self.bind("<Triple-1>", lambda event: "break", '+')

        if textvariable:
            self._set_text(self._textvariable.get())
            textvariable.trace("w", self._on_var_changed)
            self.bind("<<TextModified>>", self._on_text_changed, '+')

    def get_monospace_font(self, default_font):
        code_configure = default_font.configure()
        del code_configure["family"]

        code_font = font.nametofont("TkFixedFont")
        code_font.configure(**code_configure)

        code_font.configure(
            size=round(code_configure["size"] * default_font.metrics('linespace') / code_font.metrics('linespace'))
        )

        return code_font

    def _on_var_changed(self, *args):
        self._set_text(self._textvariable.get())

    def _on_text_changed(self, event):
        if self._textvariable:
            self._textvariable.set(self.get("1.0", tk.END))

    def config(self, **kwargs):
        text = kwargs.pop('text', None)

        if text is not None:
            self._set_text(text)

        if kwargs:
            super().config(**kwargs)

    def _set_text(self, text):
        self.delete("1.0", tk.END)

        tokens = self._tokenize(text)
        pos = "1.0"

        for token, style in tokens:
            self.insert(pos, token)
            end_pos = self.index(f"{pos}+{len(token)}c")

            if style:
                self.tag_add(style, pos, end_pos)
            pos = end_pos

    def _tokenize(self, text):
        pattern = (
            r'(?<!\\)(\*\*([^*]+)\*\*)|'
            r'(?<!\\)(\*([^*]+)\*)|'
            r'(?<!\\)(__([^_]+)__)|'
            r'(?<!\\)(~~([^~]+)~~)|'
            r"(?<!\\)(`([^`]+)`)"
        )
        tokens = []
        last_end = 0

        for match in re.finditer(pattern, text):
            start, end = match.span()

            if start > last_end:
                unescaped_text = self._unescape(text[last_end:start])
                tokens.append((unescaped_text, None))

            bold, italic, underline, overstrike, code \
                = match.group(1), match.group(3), match.group(5), match.group(7), match.group(9)

            if bold:
                tokens.append((self._unescape(match.group(2)), "bold"))
            elif italic:
                tokens.append((self._unescape(match.group(4)), "italic"))
            elif underline:
                tokens.append((self._unescape(match.group(6)), "underline"))
            elif overstrike:
                tokens.append((self._unescape(match.group(8)), "overstrike"))
            elif code:
                tokens.append((self._unescape(f"`{match.group(10)}`"), "code"))

            last_end = end

        if last_end < len(text):
            unescaped_text = self._unescape(text[last_end:])
            tokens.append((unescaped_text, None))

        return tokens

    def _unescape(self, text):
        return re.sub(r"\\(\*+|_+|~+|`+)", r'\1', text)

    def configure(self, **kwargs):
        return self.config(**kwargs)


class Image(Label):
    def __init__(self, *args, image=None, **kwargs):
        self._image = image
        super().__init__(*args, image=image, **kwargs)

    def config(self, *args, **kwargs):
        image = kwargs.get('image')

        if image is not None:
            self._image = image

        super().config(*args, **kwargs)

    configure = config
