import os
import requests
import zipfile
import shutil
import json
from io import BytesIO

# Your current game version
CURRENT_VERSION = "1.0.0"

# URL to your version.json
VERSION_JSON_URL = "https://yourserver.com/version.json"

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
            print(f"New version available: {latest_version}")
            install_update(update_url)
        else:
            print("Game is up to date.")
    except Exception as e:
        print(f"Update check failed: {e}")

def install_update(update_url):
    try:
        print(f"Downloading update from {update_url}...")
        response = requests.get(update_url)
        zip_file = zipfile.ZipFile(BytesIO(response.content))

        print("Extracting update...")
        # Use a temp folder
        temp_dir = "_update_temp"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)

        zip_file.extractall(temp_dir)

        print("Installing update...")
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, temp_dir)
                dest_path = os.path.join(os.getcwd(), rel_path)

                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.move(src_path, dest_path)

        shutil.rmtree(temp_dir)
        print("Update installed successfully. Please restart the game.")

    except Exception as e:
        print(f"Failed to install update: {e}")

if __name__ == "__main__":
    check_for_update()