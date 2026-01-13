# -*- coding: utf-8 -*-
import os
import shutil
import sys
import io
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# To przekieruje wszystkie błędy do pliku error_log.txt w folderze ze skryptem
log_path = os.path.join(os.path.dirname(__file__), "error_log.txt")
sys.stderr = open(log_path, "w")
sys.stdout = sys.stderr
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# get Downloads folder
FOLDER_PATH = os.path.expanduser("~/Downloads")

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

# Plik do sprawdzania czy skrypt żyje
DEBUG_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "debug_log.txt")

def log(msg):
    with open(DEBUG_LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()}: {msg}\n")

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
    if not os.path.exists(FOLDER_PATH):
        return

    # Mała pauza na wypadek gdyby plik był jeszcze zapisywany
    time.sleep(1)

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


class DownloadHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # Ignoruj foldery
        if event.is_directory:
            return

        # Wyświetl w logu (jeśli go używamy), że coś się dzieje
        filename = os.path.basename(event.src_path)

        # Ignoruj pliki tymczasowe przeglądarek
        if filename.lower().endswith((".tmp", ".crdownload", ".opdownload")):
            return

        # Jeśli cokolwiek się stało (stworzenie, zmiana, przeniesienie pliku)
        # poczekaj 1 sekundę i sprzątaj
        time.sleep(1)
        move_files()


if __name__ == "__main__":
    create_folders()
    move_files()  # Segregacja plików, które już tam były

    event_handler = DownloadHandler()
    observer = Observer()
    observer.schedule(event_handler, FOLDER_PATH, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(2)  # Krótka pętla, żeby skrypt był czujny
    except Exception as e:
        # Jeśli wystąpi błąd, spróbuj zapisać go do logu i nie wyłączaj się od razu
        if 'log_message' in globals():
            log_message(f"Błąd główny: {e}")
        observer.stop()
    observer.join()