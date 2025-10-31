# File-Renamer-GUI -- Rename files without whitespace, in TitleCase, based on file extension
# https://github.com/ajohnson-97/File-Renamer.py
# Written by Anthony Johnson

import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import os, datetime, time
from PIL import Image, ImageTk

# Allow the user to select a number of options to edit the file names and have seperate functions for each process, and a way to process them one by one or reject them if they dont apply, could put functions in a different file to refer to, to clean up the main source code.
# Re-factor code to be object oriented to simplify the widget creation code, and put file editing functions in a seperate file, but keep gui elements/functions in main source file. (To seperate logic functions from gui elements)
# Have a display message/pop-up if no files in the path contain the file extension (dont make it interrupt the program though)

# Colors
window_bg_color = "#C7C5B2"
text_box_color = "#EBEBEE"
label_frame_border_color = "#A1A192"

# Variables
extension_list = []
verbose = True

# Functions
def main_function():
    # Confirm that the user wants to run the program to rename the files (Yes returns True, No returns False)
    if messagebox.askyesno(title="Confirmation", 
                           message='Click "OK" if you are ready to rename your files. If you are not ready then click "Cancel"'):
        program_start_time_snapshot = time.perf_counter()
        """
        Content goes here
        -Create a for loop to iterate over the list of file extension parameters and process them one at a time to rename all the files with the extensions in the list.
        -Rename the files ignoring the file extension at first then append it to the end of the file so if we need to manipulate the file name based on special parameters or increment them
            then we can do so without having to find a workaround, scrap the file extension, rename the file and then append the file extension or rename the string including the file extension at the end.
        -Verify that a path is selected before the user can enter file extension filters into the entry box
        -Once a path is selected and the user enters filters into the entry box, verify that file(s) exists in the path before adding it to the list so it will automatically remove any filters that are irrelevent in the path to make processing easier.
        -Make a check box that must be selected before the user can run the program that basically says "I read the warning", could have it in a label frame with 2 tabs, the second tab would contain a text box with the warning message, or if its a short
            message then it can just fit on the screen beside the check box, or the checkbox is beside or below the scrollable textbox with the message, just dont want it ruining the layout of the app.
            
        **** Could have the existing textbox for the verbose output to contain the warning message upon program startup and then the checkbox is below it so its there to read and then it scrolls off screen as the verbose output fills the textbox
        
        """
        program_end_time_snapshot = time.perf_counter()
        completion_time = program_end_time_snapshot - program_start_time_snapshot
        # (PUT AN IF STATEMENT HERE) to check if the program actually renamed any files, or have a check to make sure that there's files in the path when they select it.
        messagebox.showinfo(title="Program Completed", message=f"Files have been renamed.\nCompletion time: {completion_time:.6f} Seconds")
    else:
        pass

def return_key_bind(event): # Check if Entry box is focused
    if root.focus_get() == search_filter_entry:
        add_extension()
    else:
        main_function()

def clear_focus(event): # Clear the window focus on left mouse click
    if event.widget != search_filter_entry:
        root.focus_set()

def quit_program(event):
    root.destroy()

def add_extension():
    ext = search_filter_entry.get().strip() # Strip the whitespace from either end of the string
    if ext: # If the user actually enters something (an empty string returns False)
        if ext[0] == ".":
            if ext in extension_list: # Check that the extension isn't already in the list (for single extension entries)
                duplicate_entry_popup = messagebox.showinfo(title="Duplicate Entry", message="That filter has already been added to the list.")
            else:
                if " " in ext: # Multiple extensions entered in one submission (by checking for spaces in the string)
                    extension_list_multiple_entry = ext.split() # Split the words/extensions into seperate elements and store them in a list
                    for single_entry in extension_list_multiple_entry: # Process each extension in the list to seperate them into individual elements
                        single_entry.strip() # Strip the whitespace from either end again, just in case the user entered two spaces or something (might not be necessary)
                        if single_entry[0] == ".":
                            if single_entry not in extension_list: # Check that an extension included in the multiple extension submission isn't already in the list (or duplicated in the multiple input entry)
                                extension_list.append(single_entry)
                            else: # Specify which extension has already been added since multiple were added at once, not needed for a single entry because you'll know what was a duplicate since you just entered it.
                                duplicate_entry_popup = messagebox.showinfo(title="Duplicate Entry", message=f"{single_entry} has already been added to the list. Removing the duplicate entry(s)")
                        else:
                            invalid_input_popup = messagebox.showinfo(title="Format Error", message="File extensions must start with a period.")
                    display_text = ", ".join(extension_list)
                    extension_confirmation.config(text=display_text)
                else:
                    extension_list.append(ext) # Add the single submission to the list
                    display_text = ", ".join(extension_list)
                    extension_confirmation.config(text=display_text)
        else:
            invalid_input_popup = messagebox.showinfo(title="Format Error.", message="File extensions must start with a period.")
    else:
        invalid_input_popup = messagebox.showerror(title="Invalid Input", message="You didn't submit anything.")
    entry_box_delete() 

def entry_box_delete(): # Clear the entry box
    search_filter_entry.delete(0,"end")

def filter_list_delete(): # Clear the list of search filters
    extension_list.clear()
    extension_confirmation.config(text=extension_list)

def filter_list_pop(): # Remove the last extension added to the list
    if len(extension_list) > 0:
        extension_list.pop()
        extension_confirmation.config(text=extension_list)
    else:
        pass

def file_path(): # Function to get/set the working directory
    path = filedialog.askdirectory()
    if os.path.exists(path):
        #os.chdir(path)
        path_confirmation.config(text=path)
    else:
        invalid_path_warning = messagebox.showerror(title="Error", message="That is not a valid path.")

def show_verbose_val(): # Funcion to set the verbose value
    global verbose
    if verbose_button_value.get():
        verbose = True
    else:
        verbose = False
    print(verbose, datetime.datetime.now())

def filter_status_func(): # Function to apply search filters
    global apply_filters
    #print(filter_status_var.get())
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
window_icon = tk.PhotoImage(file="assets/icon.png")
root.iconphoto(True, window_icon)
root.config(background=window_bg_color)

# Logo on Screen
logo = tk.PhotoImage(file="logo_black_dots_black_letters.png", width=250, height=145)
logo_label = tk.Label(root, image=logo, bg=window_bg_color)
logo_label.pack()

search_filter_entry = tk.Entry(root, bg=text_box_color, font=("verdana",10))
search_filter_entry.pack()

# Path Button Image
path_icon_large = tk.PhotoImage(file="assets/icon.png")
path_icon = path_icon_large.subsample(24, 24)
path_icon_button = tk.Button(root, image=path_icon, command=file_path, bg=window_bg_color, border=0)
path_icon_button.pack()

# Label Frames
label_frame_path = tk.LabelFrame(root, text="Filters", bg=window_bg_color)
label_frame_path.pack(padx=20, pady=20, ipadx=50, ipady=50, expand=True)

# Labels
extension_confirmation = tk.Label(root, bg=window_bg_color, text="", font=("verdana",10))
extension_confirmation.pack()

path_confirmation = tk.Label(root, bg=window_bg_color, text="", font=("verdana",10))
path_confirmation.pack()

# Buttons
verbose_button_value = tk.IntVar()
verbose_mode_checkbox = tk.Checkbutton(label_frame_path, text="Verbose", compound="left", font=("verdana",10), 
                                    bg=window_bg_color, variable=verbose_button_value, onvalue=1, offvalue=0, 
                                    activebackground=window_bg_color, command=show_verbose_val)
verbose_button_value.set(1) # Set the default state of the verbose button to be on
verbose_mode_checkbox.pack()

search_filter_submission_button = tk.Button(root, text="Submit", font=("verdana",10), command=add_extension)
search_filter_submission_button.pack()

file_path_finder_button = tk.Button(root, text="Path", font=("verdana",10), command=file_path)
file_path_finder_button.pack()

extension_confirmation_clear = tk.Button(root, bg=window_bg_color, text="Clear filters", font=("verdana",10), command=filter_list_delete)
extension_confirmation_clear.pack()

extension_confirmation_pop = tk.Button(root, bg=window_bg_color, text="Remove filter", font=("verdana",10), command=filter_list_pop)
extension_confirmation_pop.pack()

# Radio buttons
filter_status_var = tk.IntVar()
radio_button_options = ["None", "Apply Filters"]
for index in range(len(radio_button_options)):
    radio_button = tk.Radiobutton(root, text=radio_button_options[index], font=("verdana",10), 
                               variable=filter_status_var, value=index, bg=window_bg_color, activebackground=window_bg_color,
                               command=filter_status_func)
    radio_button.pack(anchor="w")

start_button = tk.Button(root, text="Start", font=("verdana",10), command=main_function, padx=50) # Run the main function to rename the files
start_button.pack()

# Console Window
console_window = ScrolledText(root, bg="black", fg="#00BB00", width="80", height="10")
console_window.pack(expand=True)

# Key Bindings
root.bind("<Return>", return_key_bind) # Bind the return key
root.bind('<Button-1>', clear_focus) # Bind the left mouse click to clear the window focus
root.bind('<Escape>', quit_program) # Bind the escape key to close the window and terminate the program

root.mainloop()
