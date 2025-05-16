import os
import requests
import zipfile
import shutil
import json
from io import BytesIO

CURRENT_VERSION = "InDev 0.0.1"
VERSION_JSON_URL = "https://github.com/brudiW/platformer/blob/main/version.json"
ALLOWED_UPDATE_EXTENSIONS = {".py", ".pyc", ".pyo"}  # Only game logic
ALLOWED_UPDATE_FOLDERS = {"", "src", "core", "engine"}  # Adjust to match your code structure

def is_code_file(path):
    _, ext = os.path.splitext(path)
    return ext in ALLOWED_UPDATE_EXTENSIONS

def is_in_allowed_folder(path):
    top_level = os.path.normpath(path).split(os.sep)[0]
    return top_level in ALLOWED_UPDATE_FOLDERS

def check_for_update():
    try:
        print("Checking for updates...")
        response = requests.get(VERSION_JSON_URL)
        data = response.json()

        latest_version = data.get("latest_version")
        update_url = data.get("update_url")

        if latest_version is None or update_url is None:
            print("Invalid version data.")
            return

        if latest_version != CURRENT_VERSION:
            print(f"Update available: {latest_version}")
            install_update(update_url)
        else:
            print("Game is up to date.")
    except Exception as e:
        print(f"Update check failed: {e}")

def install_update(update_url):
    try:
        print("Downloading update...")
        response = requests.get(update_url)
        zip_file = zipfile.ZipFile(BytesIO(response.content))

        print("Extracting update to temporary folder...")
        temp_dir = "_update_temp"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        zip_file.extractall(temp_dir)

        print("Applying update...")
        for root, _, files in os.walk(temp_dir):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), temp_dir)
                if is_code_file(rel_path) and is_in_allowed_folder(rel_path):
                    src_path = os.path.join(root, file)
                    dest_path = os.path.join(os.getcwd(), rel_path)
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.move(src_path, dest_path)
                    print(f"Updated: {rel_path}")

        shutil.rmtree(temp_dir)
        print("Game code updated. Please restart the game.")

    except Exception as e:
        print(f"Failed to install update: {e}")

if __name__ == "__main__":
    check_for_update()
