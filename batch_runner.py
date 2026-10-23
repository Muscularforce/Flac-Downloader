import os
import subprocess
import time
import requests
import shutil

SLSKD_URL = "http://localhost:5030"
API_KEY = "antigravity1234567890"

def get_headers():
    return {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }

print("Running downloader.py to queue all songs...")
subprocess.run(["python", "downloader.py"])

print("All songs queued! Waiting for downloads to complete...")
downloads_url = f"{SLSKD_URL}/api/v0/transfers/downloads"

while True:
    time.sleep(5)
    try:
        res = requests.get(downloads_url, headers=get_headers())
        if res.status_code == 200:
            active = False
            for user in res.json():
                # If there are any directories, it means there are active transfers or queued items
                if user.get("directories"):
                    for dir_info in user.get("directories", []):
                        for file_info in dir_info.get("files", []):
                            state = file_info.get("state", "")
                            # Check if it's still downloading or queued
                            if "Completed" not in state and "Cancelled" not in state and "Errored" not in state:
                                active = True
                                break
            
            if not active:
                print("All downloads finished!")
                break
            else:
                print("Downloads still in progress...")
    except Exception as e:
        print(f"Error checking status: {e}")

# Move files to target folder
source_dir = r"C:\Users\Jovan Fernandes\AppData\Local\slskd\downloads"
target_dir = r"C:\Users\Jovan Fernandes\OneDrive\Desktop\AkamoPlaylist"

print(f"Moving files from {source_dir} to {target_dir}")
os.makedirs(target_dir, exist_ok=True)
moved_count = 0
for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.endswith(('.flac', '.mp3', '.wav', '.m4a')):
            src = os.path.join(root, file)
            dst = os.path.join(target_dir, file)
            # handle duplicates
            base, ext = os.path.splitext(file)
            counter = 1
            while os.path.exists(dst):
                dst = os.path.join(target_dir, f"{base}_{counter}{ext}")
                counter += 1
            
            shutil.move(src, dst)
            moved_count += 1
            print(f"Moved {file}")

print(f"Successfully moved {moved_count} songs to {target_dir}")
