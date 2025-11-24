from tkinter.scrolledtext import ScrolledText
from modules import styles
import tkinter as tk
#import state

# Add relevant arguments/parameters for specific widgets, example: active fg/bg for buttons, size/geometry for buttons/labels etc...
# Add defaults (kwargs) and layout/layout kwargs to styles file and import them into here to use so that i don't need to update each
# class to make padding changes but can do it all from styles.py but can still override values at the class level before needing to do it at the object level.

class Positioning:
    def _apply_layout(self, layout, layout_kwargs):
        layout_kwargs = layout_kwargs or {}

        if layout == "pack":
            self.pack(**layout_kwargs)
        elif layout == "grid":
            self.grid(**layout_kwargs)
        elif layout == "place":
            self.place(**layout_kwargs)
        elif layout == "none":
            pass  # No layout applied
        else:
            raise ValueError(f"Unknown layout mode: {layout}")

class MyLabel(tk.Label, Positioning):
    def __init__(self, parent=None, text="", layout="grid", layout_kwargs=None, **kwargs):
        # If no parent passed, use the default root
        if parent is None:
            parent = tk._default_root   # Tkinter automatically tracks `root`

        defaults = {
            "font": (styles.LightTheme.font_style, styles.LightTheme.font_size),
            "bg": styles.LightTheme.window_bg_color,
            "fg": "black",
            "highlightthickness": 0
        }
        defaults.update(kwargs)

        super().__init__(parent, text=text, **defaults)

        # Now apply automatic layout
        self._apply_layout(layout, layout_kwargs)
        #state.self = self

class MyLabelFrame(tk.LabelFrame, Positioning):
    def __init__(self, parent=None, text="", layout="grid", layout_kwargs=None, **kwargs):
        # If no parent passed, use the default root
        if parent is None:
            parent = tk._default_root   # Tkinter automatically tracks `root`

        defaults = {
            "font": (styles.LightTheme.font_style, styles.LightTheme.font_size),
            "bg": styles.LightTheme.window_bg_color,
            "fg": "black"
        }
        defaults.update(kwargs)

        super().__init__(parent, text=text, **defaults)

        # Now apply automatic layout
        self._apply_layout(layout, layout_kwargs)

class MyRadioButton(tk.Radiobutton, Positioning):
    def __init__(self, parent=None, text="", command=None, layout="grid", layout_kwargs=None, **kwargs):
        if parent is None:
            parent = tk._default_root

        defaults = {
            "font": (styles.LightTheme.font_style, styles.LightTheme.font_size),
            "bg": styles.LightTheme.window_bg_color,
            "activebackground": styles.LightTheme.window_bg_color,
            "highlightthickness": 0
        }
        defaults.update(kwargs)

        super().__init__(parent, text=text, command=command, **defaults)
        self._apply_layout(layout, layout_kwargs)

class MyScrolledTextBox(ScrolledText, Positioning):
    def __init__(self, parent=None, command=None, layout="grid", layout_kwargs=None, **kwargs):
        if parent is None:
            parent = tk._default_root

        defaults = {
            "width": "64",
            "height": "8",
            "font": (styles.LightTheme.console_font_style, styles.LightTheme.font_size),
            "bg": "black",
            "fg": "#00BB00",
            "insertbackground": "#00BB00",

        }
        defaults.update(kwargs)

        super().__init__(parent, command=command, **defaults)
        self._apply_layout(layout, layout_kwargs)

class MyButton(tk.Button, Positioning):
    def __init__(self, parent=None, text="", command=None, layout="grid", layout_kwargs=None, **kwargs):
        if parent is None:
            parent = tk._default_root

        defaults = {
            "font": (styles.LightTheme.font_style, styles.LightTheme.font_size),
            "bg": "#D9D9D9",
            "activebackground": "#D9D9D9",
            "fg": "black",
            "highlightthickness": 0
        }
        defaults.update(kwargs)

        super().__init__(parent, text=text, command=command, **defaults)
        self._apply_layout(layout, layout_kwargs)

class MyCheckButton(tk.Checkbutton, Positioning):
    def __init__(self, parent=None, text="", command=None, layout="grid", layout_kwargs=None, **kwargs):
        if parent is None:
            parent = tk._default_root

        defaults = {
            "font": (styles.LightTheme.font_style, styles.LightTheme.font_size),
            "bg": styles.LightTheme.window_bg_color,
            "activebackground": styles.LightTheme.window_bg_color,
            "fg": "black",
            "highlightthickness": 0
        }
        defaults.update(kwargs)

        super().__init__(parent, text=text, command=command, **defaults)
        self._apply_layout(layout, layout_kwargs)

class MyEntry(tk.Entry, Positioning):
    def __init__(self, parent, layout="grid", layout_kwargs=None, **kwargs):
        if parent is None:
            parent = tk._default_root

        defaults = {
            "font": (styles.LightTheme.font_style, styles.LightTheme.font_size),
            "bg": styles.LightTheme.text_box_color,
            "fg": "black",
            "width": 50
        }
        defaults.update(kwargs)

        super().__init__(parent, **defaults)
        self._apply_layout(layout, layout_kwargs)

if __name__ == '__main__':
    print('Run "main.py" directly. This is a module.')