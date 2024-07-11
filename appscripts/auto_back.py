import os
import shutil
import logging
from datetime import datetime

# Function to create directories if they don't exist


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Function to configure logging


def configure_logging():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    create_directory(log_dir)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    log_file = os.path.join(log_dir, f"{timestamp}.log")

    logging.basicConfig(
        filename=log_file,
        filemode='w',
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )

    return log_file

# Function to move files based on type


def move_files_based_on_type(source_folder, dest_dir):
    # Define target folder names
    folder_names = {
        "Images": ["jpg", "jpeg", "png", "gif", "bmp", "tiff"],
        "Softwares": ["dmg"],
        "Musics": ["mp3", "wav", "aac", "flac"],
        "Documents": ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt"],
        "Others": []
    }

    # Create target folders
    for folder_name in folder_names:
        create_directory(os.path.join(dest_dir, folder_name))

    # Traverse files and move based on type
    for file_name in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file_name)
        if os.path.isfile(file_path):
            file_extension = file_name.split(".")[-1].lower()

            dest_folder = "Others"
            for folder_name, extensions in folder_names.items():
                if file_extension in extensions:
                    dest_folder = folder_name
                    break

            dest_folder_path = os.path.join(dest_dir, dest_folder)
            dest_file_path = os.path.join(dest_folder_path, file_name)

            # Log file move attempt
            try:
                # Check if file exists in target location and delete if so
                if os.path.exists(dest_file_path):
                    os.remove(dest_file_path)

                # Move file
                shutil.move(file_path, dest_folder_path)
                logging.info(f"Success: {file_path} -> {dest_file_path}")
            except Exception as e:
                logging.error(
                    f"Failed: {file_path} -> {dest_file_path}, Reason: {e}")


if __name__ == "__main__":
    # Update this to your source folder path
    source_folder = "/Users/jiyongfeng/Downloads"
    # Update this to your destination directory path
    dest_dir = "/Users/jiyongfeng/Documents"

    if os.path.isdir(source_folder):
        log_file1 = configure_logging()
        move_files_based_on_type(source_folder, dest_dir)
        print(f"Log file created at: {log_file1}")
    else:
        print("No input path provided.")
