# File-Renamer-GUI -- Batch-rename files based on file extension.
# https://github.com/ajohnson-97/File-Renamer.py
# Written by Anthony Johnson

import tkinter as tk
from tkinter import ttk
from tkinter.constants import SUNKEN
import modules.styles as styles
import modules.widgets as widgets
import modules.state as state
import modules.utils as utils
import modules.ui_helpers as ui_helpers

# ======================================================================================================================
# Window Initialization
root = tk.Tk()
state.root = root

#ADD SCROLLBAR TO WINDOW(S) FOR ACCESSIBILITY IF SOMEONE CANT EXTEND THE WINDOW ALL THE WAY TO SHOW ALL THE WIDGETS IN
#THEIR WINDOW

# Window Config Parameters
root.geometry("1300x1000")
root.resizable(True, True)
root.title("File-Renamer.py")
root_icon = tk.PhotoImage(file="assets/icon.png")
root.iconphoto(True, root_icon)
root.config(background=styles.LightTheme.window_bg_color)

# Photo Images
logo_png = tk.PhotoImage(file="assets/main_app_logo.png")
state.logo_png = logo_png

path_icon_file = tk.PhotoImage(file="assets/icon_small.png")
state.path_icon_file = path_icon_file
#path_icon_resized = path_icon_large.subsample(24, 24)

window_style_ttk = ttk.Style()
window_style_ttk.theme_use('clam')
# 1. Notebook background (the grey bar behind tabs)
window_style_ttk.configure("TNotebook", background=styles.LightTheme.window_bg_color, borderwidth=0)
# 2. Notebook "client area" (where tabs display content)
window_style_ttk.configure("TNotebook.Client", background=styles.LightTheme.window_bg_color)
# Tab background (normal and selected)
window_style_ttk.configure("TNotebook.Tab", background=styles.LightTheme.window_bg_color, padding=[10, 5])  # ensures the
                                                                                               # colored area is visible
window_style_ttk.map("TNotebook.Tab", background=[("selected", styles.LightTheme.window_bg_color),
                                                  ("active", styles.LightTheme.window_bg_color)])

window = ttk.Notebook(root)
tab1 = tk.Frame(window, bg=styles.LightTheme.window_bg_color)
tab2 = tk.Frame(window, bg=styles.LightTheme.window_bg_color)
tab3 = tk.Frame(window, bg=styles.LightTheme.window_bg_color)
window.add(tab1,text="Home")
window.add(tab2,text="Documentation")
window.add(tab3,text="Credits")
window.pack(expand=True,fill="both") # Expand fills any space not otherwise used, fill, fills the space on x-y axis

# TAB 1 ================================================================================================================
logo_label_tab1 = widgets.MyLabel(tab1, image=logo_png, layout_kwargs={"row": 0, "column": 0, "columnspan": 2, "pady": 25})
state.logo_label_tab1 = logo_label_tab1

path_border_frame = widgets.MyLabelFrame(tab1, text="Directory", layout_kwargs={"row": 1, "column": 0, "padx": 50, "pady": 15, "ipadx": 10, "ipady": 5, "sticky": "w"})
state.path_border_frame = path_border_frame

path_label = widgets.MyLabel(path_border_frame, text="Path:", layout_kwargs={"row": 0, "column": 0, "padx": 5})
state.path_label = path_label

path_entry_box = widgets.MyEntry(path_border_frame, width=50, layout_kwargs={"row": 0, "column": 1, "padx": 5})
state.path_entry_box = path_entry_box

path_icon_button = widgets.MyButton(path_border_frame, image=path_icon_file, command=utils.get_path_from_button, border=None, bg=styles.LightTheme.window_bg_color, layout_kwargs={"row": 0, "column": 2, "padx": 5})
state.path_icon_button = path_icon_button

log_button_value = tk.IntVar()
state.log_button_value = log_button_value
log_button_checkbox = widgets.MyCheckButton(path_border_frame, text="Generate a log file", variable=log_button_value, onvalue=1, offvalue=0, command=ui_helpers.log_file_radio_buttons_status, layout_kwargs={"row": 1, "column": 0, "columnspan": 2, "sticky": "w", "padx": 0, "pady": 5})
state.log_button_checkbox = log_button_checkbox
log_button_value.set(1)  # Set the default state of the verbose button to be on
log_file_location_var = tk.StringVar(value="default")
state.log_file_location_var = log_file_location_var
log_file_same_path = widgets.MyRadioButton(path_border_frame, text="Place log file in working directory", variable=log_file_location_var, value="default", command=ui_helpers.log_file_radio_buttons_status, layout_kwargs={"row": 2, "column": 0, "columnspan": 2, "padx": 5})
state.log_file_same_path = log_file_same_path
log_file_custom_path = widgets.MyRadioButton(path_border_frame, text="Place log file in an alternate location", variable=log_file_location_var, value="custom", command=ui_helpers.log_file_radio_buttons_status, layout_kwargs={"row": 3, "column": 0, "columnspan": 2, "padx": 5})
state.log_file_custom_path = log_file_custom_path
custom_log_location_entry_box = widgets.MyEntry(path_border_frame, width=50, layout_kwargs={"row": 4, "column": 0, "columnspan": 2, "padx": 5})
state.custom_log_location_entry_box = custom_log_location_entry_box
custom_log_path_button = widgets.MyButton(path_border_frame, image=path_icon_file, command=utils.get_log_path_from_button, border=None, bg=styles.LightTheme.window_bg_color, layout_kwargs={"row": 4, "column": 2, "padx": 5})
state.custom_log_path_button = custom_log_path_button

filters_border_frame = widgets.MyLabelFrame(tab1, text="Apply To", layout_kwargs={"row": 1, "column": 1, "padx": 50, "pady": 15, "ipadx": 14, "ipady": 10, "sticky": "w"})
state.filters_border_frame = filters_border_frame

ext_filter_status = tk.StringVar(value="disable")
state.ext_filter_status = ext_filter_status

apply_all_radio_button = widgets.MyRadioButton(filters_border_frame, text="All Files", variable=ext_filter_status, value="disable", command=ui_helpers.apply_filters, layout_kwargs={"row": 0, "column": 0, "padx": 5})
state.apply_all_radio_button = apply_all_radio_button

filter_by_ext_radio_button = widgets.MyRadioButton(filters_border_frame, text="Filter By Extension", variable=ext_filter_status, value="enable", command=ui_helpers.apply_filters, layout_kwargs={"row": 0, "column": 1, "padx": 5, "pady": 10})
state.filter_by_ext_radio_button = filter_by_ext_radio_button

ext_entry_label = widgets.MyLabel(filters_border_frame, text="Add Extension:", layout_kwargs={"row": 1, "column": 0, "padx": 5})
state.ext_entry_label = ext_entry_label

ext_entry_field = widgets.MyEntry(filters_border_frame, width=40, layout_kwargs={"row": 1, "column": 1, "padx": 5, "pady": 10})
state.ext_entry_field = ext_entry_field

ext_entry_button = widgets.MyButton(filters_border_frame, text="Add", command=utils.add_extension, layout_kwargs={"row": 1, "column": 2, "padx": 5})
state.ext_entry_button = ext_entry_button

ext_display_clear = widgets.MyButton(filters_border_frame, text="Clear List", command=utils.filter_list_delete, layout_kwargs={"row": 2, "column": 1, "sticky": "w", "padx": 5})
state.ext_display_clear = ext_display_clear

ext_display_remove = widgets.MyButton(filters_border_frame, text="Delete Item", command=utils.filter_list_pop, layout_kwargs={"row": 2, "column": 1, "sticky": "e", "padx": 5})
state.ext_display_remove = ext_display_remove

ext_list_label = widgets.MyLabel(filters_border_frame, text="Filter List:", layout_kwargs={"row": 3, "column": 0, "padx": 5})
state.ext_list_label = ext_list_label

ext_display_list = widgets.MyLabel(filters_border_frame, border=1, bg=styles.LightTheme.text_box_color, relief=SUNKEN, width=25, layout_kwargs={"row": 3, "column": 1, "padx": 5, "pady": 10})
state.ext_display_list = ext_display_list

console_window = widgets.MyScrolledTextBox(tab1, layout_kwargs={"row": 3, "column": 0, "columnspan": 2, "padx": 50, "pady": 15})
state.console_window = console_window

start_button = widgets.MyButton(tab1, text="Start", command=utils.run_program,  padx=50, layout_kwargs={"row": 4, "column": 0, "columnspan": 2, "padx": 50, "pady": 15})  # Run the main function to rename the files
state.start_button = start_button

# TAB 2 ================================================================================================================
#logo_label_tab2 = widgets.MyLabel(tab2, image=logo_png, layout="pack", layout_kwargs={"pady": 25})
#state.logo_label_tab2 = logo_label_tab2

instructions_frame = widgets.MyLabelFrame(tab2, text="Instructions", width=600, height=300, layout_kwargs={"row": 0, "column": 0, "padx": 50})
state.instructions_frame = instructions_frame

liability_frame = widgets.MyLabelFrame(tab2, text="Liability Notice", width=600, height=300, layout_kwargs={"row": 0, "column": 1, "pady": 50})
state.liability_frame = liability_frame


# TAB 3 ================================================================================================================
logo_label_tab3 = widgets.MyLabel(tab3, image=logo_png, layout="pack", layout_kwargs={"pady": 25})
state.logo_label_tab3 = logo_label_tab3

credits_label = widgets.MyLabel(tab3, text="Built entirely with Python and the tkinter GUI library. Developed by \
Anthony Johnson.\nThank you for supporting Free and Open Source Software (FOSS).", font=("Verdana", 12), layout="pack", width=600, pady=25, layout_kwargs={"pady": 50})

bug_report_button = widgets.MyButton(tab3, text="Submit a bug report", layout="pack", padx=15, pady=8, command=utils.open_link)

# ======================================================================================================================

# Key Bindings
root.bind("<Return>", ui_helpers.return_key_bind)  # Bind the return key
root.bind("<Button-1>", ui_helpers.clear_focus, add="+")
root.bind('<Escape>', ui_helpers.quit_program)  # Bind the escape key to close the window and terminate the program

# Bind events to the existing entry widget
ext_entry_field.bind("<FocusIn>", ui_helpers.remove_ext_placeholder_text)
ext_entry_field.bind("<FocusOut>", ui_helpers.set_ext_placeholder_text)
console_window.bind("<Key>", lambda x: "break")
path_entry_box.bind("<Return>", ui_helpers.return_key_path_entry)
path_entry_box.bind("<FocusIn>", ui_helpers.remove_path_placeholder_text)
path_entry_box.bind("<FocusOut>", ui_helpers.set_path_placeholder_text)
custom_log_location_entry_box.bind("<FocusIn>", ui_helpers.set_custom_log_path_placeholder_text)
custom_log_location_entry_box.bind("<FocusOut>", ui_helpers.remove_custom_log_path_placeholder_text)

utils.console_print("\n ========== FILE RENAMER CONSOLE ===============\n")
# Set the placeholder initially
ui_helpers.set_ext_placeholder_text(None)
ui_helpers.set_path_placeholder_text(None)
ui_helpers.apply_filters()
#if state.verbose:
    #utils.console_print(" > Generating a log file")

# ======================================================================================================================

if __name__ == '__main__':
    root.mainloop()
else:
    print('Run main.py directly, it is not a module.')

# BUGS -----------------------------------------------------------------------------------------------------------------

# FEATURES TO ADD ------------------------------------------------------------------------------------------------------
#   Secondary page with license, liability warning, credits, bug report button/link, GitHub page button/link, support
#   FOSS message - Include some of this stuff in GitHub readme file.
#
#