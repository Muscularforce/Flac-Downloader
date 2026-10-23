import os
import sys
import subprocess
import time
import requests
import shutil
from config import SLSKD_URL, get_headers, SOURCE_DIR, TARGET_DIR, PREFERRED_EXTENSIONS, validate_config

validate_config()

print("=" * 60)
print("🎵 FLAC Downloader — Batch Runner")
print(f"📁 SLSKD Download Folder : {SOURCE_DIR}")
print(f"🎯 Target Move Folder    : {TARGET_DIR}")
print("=" * 60)

print("\n🚀 Step 1: Queuing all songs from playlist...")
subprocess.run([sys.executable, "downloader.py"])

print("\n⏳ Step 2: Waiting for slskd downloads to finish...")
downloads_url = f"{SLSKD_URL}/api/v0/transfers/downloads"

while True:
    time.sleep(5)
    try:
        res = requests.get(downloads_url, headers=get_headers())
        if res.status_code == 200:
            active = False
            active_count = 0
            for user in res.json():
                if user.get("directories"):
                    for dir_info in user.get("directories", []):
                        for file_info in dir_info.get("files", []):
                            state = file_info.get("state", "")
                            # Check if still downloading or queued
                            if "Completed" not in state and "Cancelled" not in state and "Errored" not in state:
                                active = True
                                active_count += 1
            
            if not active:
                print("\n✅ All downloads completed!")
                break
            else:
                print(f"⏳ In progress ({active_count} file(s) downloading/queued)...")
    except Exception as e:
        print(f"⚠️ Error checking status: {e}")

print(f"\n🚚 Step 3: Moving completed songs to {TARGET_DIR}...")
os.makedirs(TARGET_DIR, exist_ok=True)
moved_count = 0

for root, dirs, files in os.walk(SOURCE_DIR):
    for file in files:
        if file.lower().endswith(tuple(PREFERRED_EXTENSIONS)):
            src = os.path.join(root, file)
            dst = os.path.join(TARGET_DIR, file)
            
            # Handle filename duplicates
            base, ext = os.path.splitext(file)
            counter = 1
            while os.path.exists(dst):
                dst = os.path.join(TARGET_DIR, f"{base}_{counter}{ext}")
                counter += 1
            
            try:
                shutil.move(src, dst)
                moved_count += 1
                print(f"  -> Moved: {file}")
            except Exception as e:
                print(f"  -> Could not move {file}: {e}")

print(f"\n🎉 Finished! Successfully moved {moved_count} song(s) to '{TARGET_DIR}'.")
