from styles import *
import tkinter as tk

class Label(tk.Label):
    def __init__(self, parent, text="", layout="pack", layout_kwargs=None, **kwargs):
        defaults = {
            "font": (LightTheme.text_font, LightTheme.text_font_size),
            "bg": LightTheme.window_bg_color,
            "fg": "black"
        }
        defaults.update(kwargs)

        super().__init__(parent, text=text, **defaults)

        # Now apply automatic layout
        self._apply_layout(layout, layout_kwargs)

    def _apply_layout(self, layout, layout_kwargs):
        if layout == "pack":
            self.pack(**(layout_kwargs or {}))
        elif layout == "grid":
            self.grid(**(layout_kwargs or {}))
        elif layout == "place":
            self.place(**(layout_kwargs or {}))
        elif layout == "none":
            pass  # skip layout
        else:
            raise ValueError(f"Unknown layout mode: {layout}")


if __name__ == '__main__':
    print('Run "main.py" directly. This is a module.')