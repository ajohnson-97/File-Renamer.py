# File-Renamer.py -- Rename files without whitespace, in TitleCase, based on file extension
# https://github.com/ajohnson-97/File-Renamer.py
# Written by Anthony Johnson

import os
while True:
    try:
        path = input("Enter the absolute path to the directory you want to edit: ")
        if os.path.exists(path):
            os.chdir(path)
            break
        else:
            print("That path does not exist, please try again or press CTRL + c to quit.\n")
    except KeyboardInterrupt:
        print("\nGoodbye!")
        quit()

file_extension = input("\nEnter the file extension of the files you wish to rename: ")
print("\nEnter the character you'd like to replace the whitespaces with, ")
delimiter_character = input("Press enter to choose no character: ")
verbose = input("\nPress 1 for verbose mode or 0 to skip: ")
print()

summary = "File Renaming Summary: \n"
counter = 0

for file in os.listdir():
    if file == "File Renaming Summary.txt":
        pass
    elif file.endswith(file_extension):
        new_name = delimiter_character.join(file.title().split())
        if verbose:
            print(f"Renamed {file} to {new_name}\n")
        os.rename(file, new_name)
    else:
        counter += 1
        summary += f"Couldn't rename {file} because it's not a {file_extension} file.\n"
        if verbose:
            print(f"Error: Couldn't rename {file}\n")

if os.path.exists(f"{path}\\File Renaming Summary.txt"):
    with open("File Renaming Summary.txt", "a") as f:
        f.write(f"\n\nNewest Update: \n\n{summary}")
else:
    f = open("File Renaming Summary.txt", "x")
    f.close()
    f = open("File Renaming Summary.txt", "w")
    f.write(summary)
    f.close()

print(f"All Done! With {counter} error(s).")
if counter > 0:
    print(f'Check the "File Renaming Summary.txt" located in {path}for details.')
print("Thank you, Goodbye.\n")
