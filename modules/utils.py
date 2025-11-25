from modules import state, styles
import tkinter as tk
from tkinter import messagebox, filedialog
import datetime, time, os
import webbrowser

# Functions
def run_program():
    state.start_button.config(state=tk.DISABLED) # Disable the start button while the program is running
    # Confirm that the user wants to run the program to rename the files (Yes returns True, No returns False)
    # Have a display message/pop-up if no files in the path contain the file extension
    # Allow the user to select a number of options to edit the file names and have separate functions for each process,
    # and a way to process them one by one or reject them if they don't apply.
    path = get_path_from_text() # Get the file path
    # os.chdir(path) UNCOMMENT WHEN READY TO START TESTING
    if not path: # If the file path returned is invalid
        state.start_button.config(state=tk.NORMAL)  # Re-enable the start button after the program finishes
        return # Exit the run_program function

    log_file_path_status()
    if not state.log_path:
        state.start_button.config(state=tk.NORMAL)  # Re-enable the start button after the program finishes
        return

    console_print(f"\n > Confirming the path:\n > Target Directory: {state.path_entry_box.get().strip()}")
    '''
        if len(state.ext_display_list) > 0:
            console_print(f"    * Applying File Extension Filters: {state.ext_display_list}")
        else:
            console_print(f"    * Renaming All Files In The Directory:")
        console_print("\n > ONCE YOU RUN THE PROGRAM IT CANNOT BE UNDONE\n > CLICK CANCEL IF YOU ARE UNSURE")
    '''
    if messagebox.askokcancel(title="Confirmation",
                           message='Click "OK" if you are ready to rename your files. If you are not ready then click \
                                    "Cancel"'):
        console_print("\n ========== BEGIN RENAMING PROCESS ==========")
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
    else:
        console_print(" > Program Cancelled")
    state.start_button.config(state=tk.NORMAL) # Re-enable the start button after the program finishes

def add_extension():
    try:
        ext_filter_input = state.ext_entry_field.get().strip()  # Get input from the user through the search filter box
        #assert ext_filter_input  # Verify that the value isn't False, zero, an empty string or None
        if ext_filter_input == "" or ext_filter_input == state.placeholder_text:
            messagebox.showerror("Invalid Input", "You didn't submit anything.")
            state.ext_entry_field.delete(0, tk.END)
            state.ext_entry_field.config(fg="black")
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
        state.ext_entry_field.config(fg="black")  # Return entry box input text to black after errors

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
            if ext in state.extension_list:
                if multiple_entries:
                    raise KeyError(f"{ext} has already been added to the list. Removing the duplicate entry(s).")
                else:
                    raise KeyError("That filter has already been added to the list.")

            # Add it to both lists
            state.extension_list.append(ext)
            console_print(f" > Adding {ext} to the extension list")
            seen_this_entry.add(ext)

        except ValueError as value_error:
            messagebox.showinfo(title="Format Error", message=str(value_error))

        except KeyError as duplicate_error:
            messagebox.showinfo(title="Duplicate Entry", message=str(duplicate_error))

        except Exception as e:
            messagebox.showerror(title="Unexpected Error", message=f"An unexpected error occurred: {e}")
        finally:
            state.ext_entry_field.config(fg="black")  # Return entry box input text to black after errors

    # Update display
    display_text = ", ".join(state.extension_list)
    state.ext_display_list.config(text=display_text)
    ext_entry_remove()  # Clear the text entry field after each entry

def ext_entry_remove():  # Clear the entry box when the clear button is pressed
    state.ext_entry_field.delete(0, "end")

def filter_list_delete():  # Clear the list of search filters
    if len(state.extension_list) > 0:
        console_print(f" > Clearing the extension list")
    state.extension_list.clear()
    state.ext_display_list.config(text='')

def filter_list_pop():  # Remove the last extension added to the list
    if len(state.extension_list): # Check that there is an extension in the list (True == not zero length)
        console_print(f" > Removing {state.extension_list[-1]} from the extension list")
        state.extension_list.pop()
        state.ext_display_list.config(text=', '.join(state.extension_list))

def get_path_from_text():
    try:
        if (state.path_entry_box.get().strip() == ".") or (state.path_entry_box.get().strip() == ".."):
            raise Exception
        else:
            if os.path.exists(state.path_entry_box.get().strip()):
                return state.path_entry_box.get().strip()
            else:
                messagebox.showerror(title="Error", message="Path is not valid")
    except TypeError:
        pass
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Something went wrong: {e}")
        return None

def get_path_from_button():  # Function to get/set the working directory
    try:
        path = filedialog.askdirectory()
        assert path
        if os.path.exists(path):
            state.path_entry_box.config(fg="black")
            state.path_entry_box.delete(0, tk.END)
            state.path_entry_box.insert(0, path)
            console_print(f" > Target Directory: {state.path_entry_box.get().strip()}")
        else:
            messagebox.showerror(title="Error", message="That is not a valid path.")
    except AssertionError:
        return

def show_log_val():  # Function to set the verbose value
    if state.log_button_value.get():
        state.verbose = True
        console_print(" > Generating a log file")
    else:
        state.verbose = False
        console_print(" > Opted out of logging")
    print(state.verbose, datetime.date.today())

def log_file_path_status():
    if state.log_file_location_var.get() == "custom":
        return get_log_path_from_text()
    else:
        return get_path_from_text()

def get_log_path_from_text():
    try:
        if (state.custom_log_location_entry_box.get().strip() == ".") or (state.custom_log_location_entry_box.get().strip() == ".."):
            raise Exception
        else:
            if os.path.exists(state.custom_log_location_entry_box.get().strip()):
                return state.custom_log_location_entry_box.get().strip()
            else:
                messagebox.showerror(title="Error", message="Path is not valid")
                state.custom_log_location_entry_box.config(state=tk.NORMAL)
                state.custom_log_location_entry_box.config(bg=styles.LightTheme.text_box_color, fg="black")
                return None
    except TypeError:
        pass
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Something went wrong: {e}")
        state.custom_log_location_entry_box.config(state=tk.NORMAL)
        state.custom_log_location_entry_box.config(bg=styles.LightTheme.text_box_color, fg="black")
        return None

def get_log_path_from_button():  # Function to get/set the working directory
    try:
        path = filedialog.askdirectory()
        assert path
        if os.path.exists(path):
            state.custom_log_location_entry_box.config(fg="black")
            state.custom_log_location_entry_box.delete(0, tk.END)
            state.custom_log_location_entry_box.insert(0, path)
            console_print(f" > Log file location: {state.custom_log_location_entry_box.get()}")
        else:
            messagebox.showerror(title="Error", message="That is not a valid path.")
    except AssertionError:
        return

def console_print(message):
    state.console_window.config(state=tk.NORMAL)      # enable editing
    state.console_window.insert(tk.END, message + "\n")
    state.console_window.see(tk.END)                  # auto-scroll to bottom
    state.console_window.config(state=tk.DISABLED)    # prevent user edits

def open_link():
    webbrowser.open("https://github.com/ajohnson-97/File-Renamer.py/issues")

if __name__ == '__main__':
    print('Run "main.py" directly. This is a module.')
