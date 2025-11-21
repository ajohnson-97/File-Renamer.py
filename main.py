# File-Renamer-GUI -- Batch-rename files based on file extension.
# https://github.com/ajohnson-97/File-Renamer.py
# Written by Anthony Johnson

import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from tkinter.constants import SUNKEN
from tkinter.scrolledtext import ScrolledText
import os, datetime, time
from modules.styles import *
from modules.widgets import *

'''
from click import command
import modules.styles
'''

# Global Variables
extension_list = []
verbose = True
placeholder_text = "  Separate by space for multiple entries"
path_placeholder_text = "  Select the folder you want to rename files under"

# Functions
def run_program():
    start_button.config(state=tk.DISABLED) # Disable the start button while the program is running
    # Confirm that the user wants to run the program to rename the files (Yes returns True, No returns False)
    # Have a display message/pop-up if no files in the path contain the file extension
    # Allow the user to select a number of options to edit the file names and have separate functions for each process,
    # and a way to process them one by one or reject them if they don't apply.
    path = get_path_from_text() # Get the file path
    if not path: # If the file path returned is invalid
        start_button.config(state=tk.NORMAL)  # Re-enable the start button after the program finishes
        return # Exit the run_program function
    if messagebox.askokcancel(title="Confirmation",
                           message='Click "OK" if you are ready to rename your files. If you are not ready then click \
                                    "Cancel"'):
        console_print(f" > Target Directory: {path_entry_box.get().strip()}")
        console_print(" ========== BEGIN RENAMING PROCESS ==========")
        program_start_snapshot = time.perf_counter()
        """
        Content goes here
        -Verify that a path was selected and filters were applied. If no filters were applied it will apply to all
        -Create a for loop to iterate over the list of file extension parameters and process them one at a time to 
            rename all the files with the extensions in the list.
        -Rename the files ignoring the file extension at first then append it to the end of the file so if we need to 
            manipulate the file name based on special parameters or increment them
            then we can do so without having to find a workaround, scrap the file extension, rename the file and then 
            append the file extension or rename the string including the file extension at the end.
        -Verify that a path is selected before the user can enter file extension filters into the entry box
        -Once a path is selected and the user enters filters into the entry box, verify that file(s) exists in the path 
            before adding it to the list so it will automatically remove any filters that are irrelevant in the path to 
            make processing easier.
        -Make a check box that must be selected before the user can run the program that basically says 
            "I read the warning", could have it in a label frame with 2 tabs, the second tab would contain a text box 
            with the warning message, or if its a short
            message then it can just fit on the screen beside the check box, or the checkbox is beside or below the 
            scrollable textbox with the message, just don't want it ruining the layout of the app.

        **** Could have the existing textbox for the verbose output to contain the warning message upon program startup
                and then the checkbox is below it so its there to read and then it scrolls off screen as the verbose 
                output fills the textbox
        """
        program_end_snapshot = time.perf_counter()
        console_print(" ========== PROCESS COMPLETE ==========\n")
        program_runtime = program_end_snapshot - program_start_snapshot
        # (PUT AN IF STATEMENT HERE) to check if the program actually renamed any files, or have a check to make sure
        # that there's files in the path when they select it.
        messagebox.showinfo(title="Program Completed",
                            message=f"Files have been renamed.\nCompletion time: {program_runtime:.6f} Seconds")
    start_button.config(state=tk.NORMAL) # Re-enable the start button after the program finishes


def return_key_bind(event):  # Check if Entry box is focused
    if root.focus_get() == ext_entry_field:
        add_extension()
    elif root.focus_get() == path_entry_box:
        get_path_from_text()
    else:
        run_program()


def clear_focus(event):
    # Widgets that SHOULD keep focus if clicked
    focus_widgets = {path_entry_box, ext_entry_field}

    # Only clear focus if user clicked somewhere else
    if event.widget not in focus_widgets:
        root.focus_set()


def path_entry_box_focus(event):
    if event.widget == path_entry_box:
        path_entry_box.focus_set()


def quit_program(event):
    if messagebox.askyesno(title='Close Program',
                           message="The ESC key was pressed, do you wish the close the program?"):  # Returns True if
        # "yes" is pressed, closing the messagebox window or clicking "no" will return False.
        root.destroy()


def add_extension():
    try:
        ext_filter_input = ext_entry_field.get().strip()  # Get input from the user through the search filter box
        #assert ext_filter_input  # Verify that the value isn't False, zero, an empty string or None
        if ext_filter_input == "" or ext_filter_input == placeholder_text:
            messagebox.showerror("Invalid Input", "You didn't submit anything.")
            ext_entry_field.delete(0, tk.END)
            ext_entry_field.config(fg="black")
            return
        if len(ext_filter_input) < 3:
            raise Exception

    except AssertionError:  # Handle empty input
        messagebox.showerror(title="Invalid Input", message="You didn't submit anything.")
        return

    except Exception as e:  # Catch-all exception handler in case an exception is thrown and not accounted for
        messagebox.showerror(title="Error", message=f"Something went wrong: {e}")
        return

    finally:
        ext_entry_remove()
        ext_entry_field.config(fg="black")  # Return entry box input text to black after errors

    # Split multiple entries by whitespace, remove duplicates from input
    extensions = ext_filter_input.split()  # Add entries to temporary list to further process
    multiple_entries = len(extensions) > 1  # If multiple extensions are added at once

    # Track which extensions were added this run (to catch duplicates entered together)
    seen_this_entry = set()

    for ext in extensions:  # Iterate through temporary list of extensions from input
        try:
            ext = ext.strip()
            if not ext.startswith("."):
                raise ValueError("File extensions must start with a period.")

            # Check if this extension was already entered in the same batch
            if ext in seen_this_entry:
                raise KeyError(f"{ext} has already been added to this filter. Removing the duplicate entry(s).")

            # Check if this extension already exists globally
            if ext in extension_list:
                if multiple_entries:
                    raise KeyError(f"{ext} has already been added to the list. Removing the duplicate entry(s).")
                else:
                    raise KeyError("That filter has already been added to the list.")

            # Add it to both lists
            extension_list.append(ext)
            console_print(f" > Adding {ext} to the extension list")
            seen_this_entry.add(ext)

        except ValueError as value_error:
            messagebox.showinfo(title="Format Error", message=str(value_error))

        except KeyError as duplicate_error:
            messagebox.showinfo(title="Duplicate Entry", message=str(duplicate_error))

        except Exception as e:
            messagebox.showerror(title="Unexpected Error", message=f"An unexpected error occurred: {e}")
        finally:
            ext_entry_field.config(fg="black")  # Return entry box input text to black after errors

    # Update display
    display_text = ", ".join(extension_list)
    ext_display_list.config(text=display_text)
    ext_entry_remove()  # Clear the text entry field after each entry


def ext_entry_remove():  # Clear the entry box when the clear button is pressed
    ext_entry_field.delete(0, "end")


def filter_list_delete():  # Clear the list of search filters
    if len(extension_list) > 0:
        console_print(f" > Clearing the extension list")
    extension_list.clear()
    ext_display_list.config(text='')


def filter_list_pop():  # Remove the last extension added to the list
    if len(extension_list): # Check that there is an extension in the list (True == not zero length)
        console_print(f" > Removing {extension_list[-1]} from the extension list")
        extension_list.pop()
        ext_display_list.config(text=', '.join(extension_list))

def get_path_from_text():
    try:
        if (path_entry_box.get().strip() == ".") or (path_entry_box.get().strip() == ".."):
            raise Exception
        else:
            if os.path.exists(path_entry_box.get().strip()):
                return path_entry_box.get().strip()
            else:
                messagebox.showerror(title="Error", message="Path is not valid")
    except TypeError:
        pass
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Something went wrong: {e}")
        return 0

def get_path_from_button():  # Function to get/set the working directory
    try:
        path = filedialog.askdirectory()
        assert path
        if os.path.exists(path):
            # os.chdir(path) UNCOMMENT WHEN READY TO START TESTING
            path_entry_box.config(fg="black")
            path_entry_box.delete(0, tk.END)
            path_entry_box.insert(0, path)
            console_print(f" > Target Directory: {path_entry_box.get().strip()}")
        else:
            messagebox.showerror(title="Error", message="That is not a valid path.")
    except AssertionError:
        return


def show_verbose_val():  # Function to set the verbose value
    global verbose
    if verbose_button_value.get():
        verbose = True
        if path_entry_box.get():
            console_print(f" > Generating a log file in {path_entry_box.get()} directory.")
        else:
            console_print(" > Generating a log file")
    else:
        verbose = False
        console_print(" > Opted out of logging")
    print(verbose, datetime.date.today())

def set_ext_placeholder_text(event):
    """Set the placeholder text if the entry is empty."""
    if ext_entry_field.get() == "":
        ext_entry_field.insert(0, placeholder_text)
        ext_entry_field.config(fg='gray')  # Placeholder color

def remove_ext_placeholder_text(event):
    """Remove the placeholder text when the entry is focused."""
    if ext_entry_field.get() == placeholder_text:
        ext_entry_field.delete(0, tk.END)
        ext_entry_field.config(fg='black')  # Change text color when the user types

def set_path_placeholder_text(event):
    """Set the placeholder text if the entry is empty."""
    if path_entry_box.get() == "":
        path_entry_box.insert(0, path_placeholder_text)
        path_entry_box.config(fg='gray')  # Placeholder color

def remove_path_placeholder_text(event):
    """Remove the placeholder text when the entry is focused."""
    if path_entry_box.get() == path_placeholder_text:
        path_entry_box.delete(0, tk.END)
        path_entry_box.config(fg='black')  # Change text color when the user types

def apply_filters():  # Function to apply search filters
    """Enable/disable extension filter fields based on radio selection."""
    if ext_filter_status.get() == "disable":  # Apply All Files
        ext_entry_label.config(state=tk.DISABLED)
        ext_entry_field.config(state=tk.DISABLED, fg="gray")  # stays gray only when disabled
        ext_entry_button.config(state=tk.DISABLED)
        ext_display_clear.config(state=tk.DISABLED)
        ext_display_remove.config(state=tk.DISABLED)
        ext_list_label.config(state=tk.DISABLED)
        ext_display_list.config(bg="lightgrey", fg="lightgray")
        console_print(" > Renaming all files in the directory")
    else:  # Filter By Extension
        ext_entry_label.config(state=tk.NORMAL)
        ext_entry_field.config(state=tk.NORMAL)

        # If placeholder text is active → keep gray, else set black
        if ext_entry_field.get() == "  Separate by space for multiple entries":
            ext_entry_field.config(fg="gray")
        else:
            ext_entry_field.config(fg="black")

        ext_entry_button.config(state=tk.NORMAL)
        ext_display_clear.config(state=tk.NORMAL)
        ext_display_remove.config(state=tk.NORMAL)
        ext_list_label.config(state=tk.NORMAL)
        ext_display_list.config(bg=LightTheme.text_box_color, fg="black")
        console_print(" > Renaming files filtered by extension")

def console_print(message):
    console_window.config(state=tk.NORMAL)      # enable editing
    console_window.insert(tk.END, message + "\n")
    console_window.see(tk.END)                  # auto-scroll to bottom
    console_window.config(state=tk.DISABLED)    # prevent user edits

def return_key_path_entry(event):
    path = get_path_from_text()
    if path: # Don't print to the console if the returned value is 0 or None
        console_print(f" > Target Directory: {path}")


# ======================================================================================================================
# Window Initialization
root = tk.Tk()

# Window Config Parameters
root.geometry("700x850")
root.resizable(True, True)
root.title("File-Renamer.py")
root_icon = tk.PhotoImage(file="assets/icon.png")
root.iconphoto(True, root_icon)
root.config(background=LightTheme.window_bg_color)

# Photo Images
logo_png = tk.PhotoImage(file="assets/main_app_logo.png")
path_icon_file = tk.PhotoImage(file="assets/icon_small.png")
#path_icon_resized = path_icon_large.subsample(24, 24)

window = ttk.Notebook(root)
tab1 = tk.Frame(window)
tab2 = tk.Frame(window)
tab3 = tk.Frame(window)
window.add(tab1,text="Main")
window.add(tab2,text="Documentation")
window.add(tab3,text="Credits")
window.pack(expand=True,fill="both")
#window.grid(row=0, column=0)
#, expand=True,fill="both")  #Expand = expand to fill any space not otherwise used. Fill = fill space on x and
                                      # y axis

logo_label = MyLabel(tab1, image=logo_png, layout_kwargs={"row": 0, "column": 0, "pady": 25})
path_border_frame = MyLabelFrame(tab1, text="Directory", layout_kwargs={"row": 1, "column": 0, "padx": 50, "pady": 15,
                                                                  "ipadx": 10, "ipady": 5, "sticky": "w"})
path_label = MyLabel(path_border_frame, text="Path:", layout_kwargs={"row": 0, "column": 0, "padx": 5})
path_entry_box = MyEntry(path_border_frame, width=50, layout_kwargs={"row": 0, "column": 1, "padx": 5})
path_icon_button = MyButton(path_border_frame, image=path_icon_file, command=get_path_from_button, border=None,
                            bg=LightTheme.window_bg_color, layout_kwargs={"row": 0, "column": 2, "padx": 5})

verbose_button_value = tk.IntVar()
verbose_mode_checkbox = MyCheckButton(path_border_frame, text="Generate a log file", compound="left",
                                      variable=verbose_button_value, onvalue=1, offvalue=0, command=show_verbose_val,
                                      layout_kwargs={"row": 1, "column": 1, "padx": 0, "pady": 5})
verbose_button_value.set(1)  # Set the default state of the verbose button to be on

filters_border_frame = MyLabelFrame(tab1, text="Apply To", layout_kwargs={"row": 2, "column": 0, "padx": 50, "pady": 15,
                                                                    "ipadx": 14, "ipady": 10, "sticky": "w"})
ext_filter_status = tk.StringVar(value="disable")
apply_all_radio_button = MyRadioButton(filters_border_frame, text="All Files", variable=ext_filter_status,
                                       value="disable", command=apply_filters, layout_kwargs={"row": 0, "column": 0,
                                                                                              "padx": 5})
filter_by_ext_radio_button = MyRadioButton(filters_border_frame, text="Filter By Extension", variable=ext_filter_status,
                                           value="enable", command=apply_filters, layout_kwargs={"row": 0, "column": 1,
                                                                                                 "padx": 5, "pady": 10})

ext_entry_label = MyLabel(filters_border_frame, text="Add Extension:", layout_kwargs={"row": 1, "column": 0, "padx": 5})
ext_entry_field = MyEntry(filters_border_frame, width=40, layout_kwargs={"row": 1, "column": 1, "padx": 5, "pady": 10})
ext_entry_button = MyButton(filters_border_frame, text="Add", command=add_extension,
                            layout_kwargs={"row": 1, "column": 2, "padx": 5})
ext_display_clear = MyButton(filters_border_frame, text="Clear List", command=filter_list_delete,
                             layout_kwargs={"row": 2, "column": 1, "sticky": "w", "padx": 5})
ext_display_remove = MyButton(filters_border_frame, text="Delete Item", command=filter_list_pop,
                              layout_kwargs={"row": 2, "column": 1, "sticky": "e", "padx": 5})
ext_list_label = MyLabel(filters_border_frame, text="Filter List:", layout_kwargs={"row": 3, "column": 0, "padx": 5})
ext_display_list = MyLabel(filters_border_frame, border=1, bg=LightTheme.text_box_color, relief=SUNKEN, width=25,
                           layout_kwargs={"row": 3, "column": 1, "padx": 5, "pady": 10})

console_window = MyScrolledTextBox(tab1, layout_kwargs={"row": 3, "column": 0, "padx": 50, "pady": 15, "sticky": "w"})
start_button = MyButton(tab1, text="Start", command=run_program, padx=50)  # Run the main function to rename the files

# ======================================================================================================================

# Key Bindings
root.bind("<Return>", return_key_bind)  # Bind the return key
root.bind("<Button-1>", clear_focus, add="+")
root.bind('<Escape>', quit_program)  # Bind the escape key to close the window and terminate the program

# Bind events to the existing entry widget
ext_entry_field.bind("<FocusIn>", remove_ext_placeholder_text)
ext_entry_field.bind("<FocusOut>", set_ext_placeholder_text)
console_window.bind("<Key>", lambda x: "break")
path_entry_box.bind("<Return>", return_key_path_entry)
path_entry_box.bind("<FocusIn>", remove_path_placeholder_text)
path_entry_box.bind("<FocusOut>", set_path_placeholder_text)

console_print("\n ========== FILE RENAMER ==========\n")
# Set the placeholder initially
set_ext_placeholder_text(None)
set_path_placeholder_text(None)
apply_filters()

# ======================================================================================================================

'''
console_print("\n ========== BEGIN RENAME PROCESS ==========\n")
console_print(f" > Target directory: {get_current_path()}")

for filename in os.listdir(get_current_path()):
    if should_process(filename):
        new_name = rename_file(filename)
        console_print(f" > Renamed: {filename} → {new_name}")
    else:
        console_print(f" > Skipped: {filename}")

console_print(" ========== PROCESS COMPLETE ==========")
'''

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