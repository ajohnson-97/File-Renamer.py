# File-Renamer-GUI -- Batch-rename files based on file extension.
# https://github.com/ajohnson-97/File-Renamer.py
# Written by Anthony Johnson

import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import os, datetime, time
from modules.styles import *

# Allow the user to select a number of options to edit the file names and have separate functions for each process, and a way to process them one by one or reject them if they don't apply, could put functions in a different file to refer to, to clean up the main source code.
# Re-factor code to be object-oriented to simplify the widget creation code, and put file editing functions in a separate file, but keep gui elements/functions in main source file. (To separate logic functions from gui elements)
# Have a display message/pop-up if no files in the path contain the file extension

# Variables
extension_list = []
verbose = True

# Functions
def run_program():
    # Confirm that the user wants to run the program to rename the files (Yes returns True, No returns False)
    if messagebox.askyesno(title="Confirmation",
                           message='Click "OK" if you are ready to rename your files. If you are not ready then click "Cancel"'):
        program_start_time_snapshot = time.perf_counter()
        """
        Content goes here
        -Verify that a path was selected and filters were applied. If no filters were applied it will apply to all
        -Create a for loop to iterate over the list of file extension parameters and process them one at a time to rename all the files with the extensions in the list.
        -Rename the files ignoring the file extension at first then append it to the end of the file so if we need to manipulate the file name based on special parameters or increment them
            then we can do so without having to find a workaround, scrap the file extension, rename the file and then append the file extension or rename the string including the file extension at the end.
        -Verify that a path is selected before the user can enter file extension filters into the entry box
        -Once a path is selected and the user enters filters into the entry box, verify that file(s) exists in the path before adding it to the list so it will automatically remove any filters that are irrelevant in the path to make processing easier.
        -Make a check box that must be selected before the user can run the program that basically says "I read the warning", could have it in a label frame with 2 tabs, the second tab would contain a text box with the warning message, or if its a short
            message then it can just fit on the screen beside the check box, or the checkbox is beside or below the scrollable textbox with the message, just don't want it ruining the layout of the app.

        **** Could have the existing textbox for the verbose output to contain the warning message upon program startup and then the checkbox is below it so its there to read and then it scrolls off screen as the verbose output fills the textbox

        """
        program_end_time_snapshot = time.perf_counter()
        completion_time = program_end_time_snapshot - program_start_time_snapshot
        # (PUT AN IF STATEMENT HERE) to check if the program actually renamed any files, or have a check to make sure that there's files in the path when they select it.
        messagebox.showinfo(title="Program Completed",
                            message=f"Files have been renamed.\nCompletion time: {completion_time:.6f} Seconds")
    else:
        pass


def return_key_bind(event):  # Check if Entry box is focused
    if root.focus_get() == search_filter_entry:
        add_extension()
    else:
        run_program()


def clear_focus(event):  # Clear the window focus on left mouse click
    if event.widget != search_filter_entry:
        root.focus_set()


def quit_program(event):
    if messagebox.askyesno(title='Close Program',
                           message="The ESC key was pressed, do you wish the close the program?"):  # Returns True if "yes" is pressed, closing the messagebox window or clicking "no" will return False.
        root.destroy()


def add_extension():
    try:
        ext_filter_input = search_filter_entry.get().strip()  # Get input from the user through the search filter box
        assert ext_filter_input  # Verify that the value isn't False, zero, an empty string or None

    except AssertionError:  # Handle empty input
        messagebox.showerror(title="Invalid Input", message="You didn't submit anything.")
        return

    except Exception as e:  # Catch-all exception handler in case an exception is thrown and not accounted for
        messagebox.showerror(title="Error", message=f"Something went wrong: {e}")
        return

    finally:
        entry_box_delete()

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
            seen_this_entry.add(ext)

        except ValueError as value_error:
            messagebox.showinfo(title="Format Error", message=str(value_error))

        except KeyError as duplicate_error:
            messagebox.showinfo(title="Duplicate Entry", message=str(duplicate_error))

        except Exception as e:
            messagebox.showerror(title="Unexpected Error", message=f"An unexpected error occurred: {e}")

    # Update display
    display_text = ", ".join(extension_list)
    extension_confirmation.config(text=display_text)
    entry_box_delete()  # Clear the text entry field after each entry


def entry_box_delete():  # Clear the entry box when the clear button is pressed
    search_filter_entry.delete(0, "end")


def filter_list_delete():  # Clear the list of search filters
    extension_list.clear()
    extension_confirmation.config(text=','.join(extension_list))


def filter_list_pop():  # Remove the last extension added to the list
    if len(extension_list): # Check that there is an extension in the list (True == not zero length)
        extension_list.pop()
        extension_confirmation.config(text=','.join(extension_list))


def file_path():  # Function to get/set the working directory
    try:
        path = filedialog.askdirectory()
        if os.path.exists(path):
            # os.chdir(path) UNCOMMENT WHEN READY TO START TESTING
            path_confirmation.config(text=path)
        else:
            messagebox.showerror(title="Error", message="That is not a valid path.")
    except TypeError:  # Handles when you close the file manager window without picking a path
        pass


def show_verbose_val():  # Function to set the verbose value
    global verbose
    if verbose_button_value.get():
        verbose = True
    else:
        verbose = False
    print(verbose, datetime.datetime.now())


def filter_status_func():  # Function to apply search filters
    #global apply_filters
    # print(filter_status_var.get())
    if filter_status_var.get():
        apply_filters = True
    else:
        apply_filters = False
    print(apply_filters)


# Window Initialization
root = tk.Tk()

# Window Config Parameters
root.geometry("1000x700")
root.resizable(True, True)
root.title("File-Renamer.py")
root_icon = tk.PhotoImage(file="assets/icon.png")
root.iconphoto(True, root_icon)
root.config(background=LightTheme.window_bg_color)

# Logo on Screen
logo = tk.PhotoImage(file="assets/logo_black_dots_black_letters.png", width=250, height=145)
logo_label = tk.Label(root, image=logo, bg=LightTheme.window_bg_color)
logo_label.pack()

search_filter_entry = tk.Entry(root, bg=LightTheme.text_box_color, font=("verdana", 10))
search_filter_entry.pack()

# Path Button Image
path_icon_large = tk.PhotoImage(file="assets/icon.png")
path_icon = path_icon_large.subsample(24, 24)
path_icon_button = tk.Button(root, image=path_icon, command=file_path, bg=LightTheme.window_bg_color, border=0)
path_icon_button.pack()

# Label Frames
label_frame_path = tk.LabelFrame(root, text="Filters", bg=LightTheme.window_bg_color)
label_frame_path.pack(padx=20, pady=20, ipadx=50, ipady=50, expand=True)

# Labels
extension_confirmation = tk.Label(root, bg=LightTheme.window_bg_color, text="", font=("verdana", 10))
extension_confirmation.pack()

path_confirmation = tk.Label(root, bg=LightTheme.window_bg_color, text="", font=("verdana", 10))
path_confirmation.pack()

# Buttons
verbose_button_value = tk.IntVar()
verbose_mode_checkbox = tk.Checkbutton(label_frame_path, text="Verbose", compound="left", font=("verdana", 10),
                                       bg=LightTheme.window_bg_color, variable=verbose_button_value, onvalue=1, offvalue=0,
                                       activebackground=LightTheme.window_bg_color, command=show_verbose_val)
verbose_button_value.set(1)  # Set the default state of the verbose button to be on
verbose_mode_checkbox.pack()

search_filter_submission_button = tk.Button(root, text="Submit", font=("verdana", 10), command=add_extension)
search_filter_submission_button.pack()

file_path_finder_button = tk.Button(root, text="Path", font=("verdana", 10), command=file_path)
file_path_finder_button.pack()

extension_confirmation_clear = tk.Button(root, bg=LightTheme.window_bg_color, text="Clear filters", font=("verdana", 10),
                                         command=filter_list_delete)
extension_confirmation_clear.pack()

extension_confirmation_pop = tk.Button(root, bg=LightTheme.window_bg_color, text="Remove filter", font=("verdana", 10),
                                       command=filter_list_pop)
extension_confirmation_pop.pack()

# Radio buttons
filter_status_var = tk.IntVar()
radio_button_options = ["None", "Apply Filters"]
for index in range(len(radio_button_options)):
    radio_button = tk.Radiobutton(root, text=radio_button_options[index], font=("verdana", 10),
                                  variable=filter_status_var, value=index, bg=LightTheme.window_bg_color,
                                  activebackground=LightTheme.window_bg_color,
                                  command=filter_status_func)
    radio_button.pack(anchor="w")

start_button = tk.Button(root, text="Start", font=("verdana", 10), command=run_program,
                         padx=50)  # Run the main function to rename the files
start_button.pack()

# Console Window
console_window = ScrolledText(root, bg="black", fg="#00BB00", width="80", height="10")
console_window.pack(expand=True)

# Key Bindings
root.bind("<Return>", return_key_bind)  # Bind the return key
root.bind('<Button-1>', clear_focus)  # Bind the left mouse click to clear the window focus
root.bind('<Escape>', quit_program)  # Bind the escape key to close the window and terminate the program

if __name__ == '__main__':
    root.mainloop()
else:
    print('Run main.py directly, it is not a module.')