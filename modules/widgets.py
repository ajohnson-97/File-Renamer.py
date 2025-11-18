from styles import *
import tkinter as tk

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

class Label(tk.Label, Positioning):
    def __init__(self, parent, text="", layout="pack", layout_kwargs=None, **kwargs):
        defaults = {
            "font": (LightTheme.font_style, LightTheme.font_size),
            "bg": LightTheme.window_bg_color,
            "fg": "black"
        }
        defaults.update(kwargs)

        super().__init__(parent, text=text, **defaults)

        # Now apply automatic layout
        self._apply_layout(layout, layout_kwargs)

class MyButton(tk.Button, Positioning):
    def __init__(self, parent, text="", command=None, layout="pack", layout_kwargs=None, **kwargs):
        defaults = {
            "font": (LightTheme.font_style, LightTheme.font_size),
            "bg": "#D9D9D9",
            "fg": "black"
        }
        defaults.update(kwargs)

        super().__init__(parent, text=text, command=command, **defaults)
        self._apply_layout(layout, layout_kwargs)


if __name__ == '__main__':
    print('Run "main.py" directly. This is a module.')