# -*- coding: utf-8 -*-
import os
import shutil
import sys
import io
from datetime import datetime

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# get Downloads folder
FOLDER_PATH = os.path.expanduser(r"C:\Users\damne\Downloads")

# create DICT with folders
FOLDERS = {
    "Images": [".gif", ".png", ".jpg", ".jpeg", ".bmp", ".svg", ".webp"],
    "Video": [".mp4", ".avi", ".mov", ".mkv", ".wmv"],
    "Audio": [".mp3", ".aac"],
    "Documents": [".pdf", "docx", ".xlsx", ".txt", ".ppt", ".pptx", ".csv"],
    "Archives": [".rar.", ".zip", ".7zip", ".tar", ".gz"],
    "Applications": [".exe"],
    "Roblox": [".rbxl"],
    "Photoshop": [".psd"],
    "Other": []
}

# creating folders function
def create_folders():
    for folder in FOLDERS:
        # create variable of path
        path = os.path.join(FOLDER_PATH, folder)

        # if path doesn't exist, create
        if not os.path.exists(path):
            os.makedirs(path)

# renaming files function
def rename_file(filename, folder):
    # splittext separates before and after '.'
    name, ext = os.path.splitext(filename)

    # get current time & format it into string
    time_stamp = datetime.now().strftime("%Y%m%d %H%M%S")

    return f"{name}_{time_stamp}{ext}"

#moving into folders function
def move_files():

    # os.listdir return list of all files within the folder
    for file in os.listdir(FOLDER_PATH):

        filepath = os.path.join(FOLDER_PATH, file)

        #errors if files dissapear before they are moved
        if os.path.isdir(filepath) or file.endswith((".tmp", ".crdownload")):
            # skip if found folder
            continue

        #move right ext into right folder

        moved = False

        file_lower = file.lower()

        #checks if ext fits DICT
        for folder, extension in FOLDERS.items():
            if file_lower.endswith(tuple(extension)):
                new_name = rename_file(file, folder)
                dest_path = os.path.join(FOLDER_PATH, folder, new_name)
                try:
                    # shutil copies/moves/archives files
                    shutil.move(filepath, dest_path)
                    print(f"________Moved: {file} -> Other/{new_name}________")
                except Exception as e:
                    print(f"Error moving {file}: {e}")
                moved = True
                break

        if not moved:
            new_name = rename_file(file, "Other")
            other_dir = os.path.join(FOLDER_PATH, "Other")
            os.makedirs(os.path.join(other_dir), exist_ok=True)
            try:
                shutil.move(filepath, os.path.join(other_dir, new_name))
                print(f"________Moved: {file} -> Other/{new_name}________")

            except Exception as e:
                print(f"Error moving {file}: {e}")


if __name__ == "__main__":
    print("Starting: download_folder_manager")
    create_folders()
    move_files()
    print("Download folder is organised.")
