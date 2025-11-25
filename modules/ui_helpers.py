from modules import state, styles, utils
import tkinter as tk
from tkinter import messagebox

def return_key_bind(event):  # Check if Entry box is focused
    if state.root.focus_get() == state.ext_entry_field:
        utils.add_extension()
    elif state.root.focus_get() == state.path_entry_box:
        utils.get_path_from_text()
    else:
        utils.run_program()

def clear_focus(event):
    # Widgets that SHOULD keep focus if clicked
    focus_widgets = {state.path_entry_box, state.custom_log_location_entry_box, state.ext_entry_field}

    # Only clear focus if user clicked somewhere else
    if event.widget not in focus_widgets:
        state.root.focus_set()

def path_entry_box_focus(event):
    if event.widget == state.path_entry_box:
        state.path_entry_box.focus_set()

def log_path_entry_box_focus(event):
    if event.widget == state.custom_log_location_entry_box:
        state.custom_log_location_entry_box.focus_set()

def quit_program(event):
    if messagebox.askyesno(title='Close Program',
                           message="The ESC key was pressed, do you wish the close the program?"):  # Returns True if
        # "yes" is pressed, closing the messagebox window or clicking "no" will return False.
        state.root.destroy()

def set_ext_placeholder_text(event):
    """Set the placeholder text if the entry is empty."""
    if state.ext_entry_field.get() == "":
        state.ext_entry_field.insert(0, state.placeholder_text)
        state.ext_entry_field.config(fg='gray')  # Placeholder color

def remove_ext_placeholder_text(event):
    """Remove the placeholder text when the entry is focused."""
    if state.ext_entry_field.get() == state.placeholder_text:
        state.ext_entry_field.delete(0, tk.END)
        state.ext_entry_field.config(fg='black')  # Change text color when the user types

def set_path_placeholder_text(event):
    """Set the placeholder text if the entry is empty."""
    if state.path_entry_box.get() == "":
        state.path_entry_box.insert(0, state.path_placeholder_text)
        state.path_entry_box.config(fg='gray')  # Placeholder color

def remove_path_placeholder_text(event):
    """Remove the placeholder text when the entry is focused."""
    if state.path_entry_box.get() == state.path_placeholder_text:
        state.path_entry_box.delete(0, tk.END)
        state.path_entry_box.config(fg='black')  # Change text color when the user types

def set_custom_log_path_placeholder_text(event):
    if state.custom_log_location_entry_box.get() == "":
        state.custom_log_location_entry_box.insert(0, state.custom_log_path_placeholder_text)
        state.custom_log_location_entry_box.config(fg='gray')

def remove_custom_log_path_placeholder_text(event):
    if state.custom_log_location_entry_box.get() == state.custom_log_path_placeholder_text:
        state.custom_log_location_entry_box.delete(0, tk.END)
        state.custom_log_location_entry_box.config(fg='black')

def apply_filters():  # Function to apply search filters
    """Enable/disable extension filter fields based on radio selection."""
    if state.ext_filter_status.get() == "disable":  # Apply All Files
        state.ext_entry_label.config(state=tk.DISABLED)
        state.ext_entry_field.config(state=tk.DISABLED, fg="gray")  # stays gray only when disabled
        state.ext_entry_button.config(state=tk.DISABLED)
        state.ext_display_clear.config(state=tk.DISABLED)
        state.ext_display_remove.config(state=tk.DISABLED)
        state.ext_list_label.config(state=tk.DISABLED)
        state.ext_display_list.config(bg="lightgrey", fg="lightgray")
        utils.console_print(" > Renaming all files in the directory")
    else:  # Filter By Extension
        state.ext_entry_label.config(state=tk.NORMAL)
        state.ext_entry_field.config(state=tk.NORMAL)

        # If placeholder text is active → keep gray, else set black
        if state.ext_entry_field.get() == "  Separate by space for multiple entries":
            state.ext_entry_field.config(fg="gray")
        else:
            state.ext_entry_field.config(fg="black")

        state.ext_entry_button.config(state=tk.NORMAL)
        state.ext_display_clear.config(state=tk.NORMAL)
        state.ext_display_remove.config(state=tk.NORMAL)
        state.ext_list_label.config(state=tk.NORMAL)
        state.ext_display_list.config(bg=styles.LightTheme.text_box_color, fg="black")
        utils.console_print(" > Renaming files using extension filter(s)")

def log_file_radio_buttons_status():
    #utils.show_log_val()
    if state.log_button_value.get():
        state.log_file_same_path.config(state=tk.NORMAL)
        state.log_file_custom_path.config(state=tk.NORMAL)
        if state.log_file_location_var.get() == "custom":
            state.custom_log_location_entry_box.config(state=tk.NORMAL)
            state.custom_log_location_entry_box.config(bg = styles.LightTheme.text_box_color)
            state.custom_log_path_button.config(state=tk.NORMAL)
            #utils.console_print(f" > Log file location: {utils.log_file_path_status()}")
            # If placeholder text is active → keep gray, else set black
            if state.ext_entry_field.get() == state.custom_log_path_placeholder_text:
                state.ext_entry_field.config(fg="gray")
            else:
                state.ext_entry_field.config(fg="black")
        else:
            state.log_file_same_path.config(state=tk.NORMAL)
            state.log_file_custom_path.config(state=tk.NORMAL)
            state.custom_log_location_entry_box.config(state=tk.DISABLED)
            state.custom_log_location_entry_box.config(fg="grey")
            state.custom_log_path_button.config(state=tk.DISABLED)
            utils.console_print(f" > Log file location: {utils.get_path_from_text()}")
    else:
        state.log_file_same_path.config(state=tk.DISABLED)
        state.log_file_custom_path.config(state=tk.DISABLED)
        state.custom_log_location_entry_box.config(state=tk.DISABLED)
        state.custom_log_path_button.config(state=tk.DISABLED)
        #state.custom_log_location_entry_box.config(fg="grey")


def return_key_path_entry(event):
    path = utils.get_path_from_text()
    if path: # Don't print to the console if the returned value is 0 or None
        utils.console_print(f" > Target Directory: {path}")