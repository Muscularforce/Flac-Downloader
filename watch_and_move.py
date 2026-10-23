import os
import shutil
import time
from config import SOURCE_DIR, TARGET_DIR, PREFERRED_EXTENSIONS

print("=" * 60)
print("👀 FLAC Downloader — Watch & Move Daemon")
print(f"📁 Watching: {SOURCE_DIR}")
print(f"🎯 Target  : {TARGET_DIR}")
print("Press Ctrl+C to stop.")
print("=" * 60)

os.makedirs(TARGET_DIR, exist_ok=True)

while True:
    if os.path.exists(SOURCE_DIR):
        for root, dirs, files in os.walk(SOURCE_DIR):
            for file in files:
                if file.lower().endswith(tuple(PREFERRED_EXTENSIONS)):
                    src = os.path.join(root, file)
                    dst = os.path.join(TARGET_DIR, file)
                    
                    # Handle duplicate filenames
                    base, ext = os.path.splitext(file)
                    counter = 1
                    while os.path.exists(dst):
                        dst = os.path.join(TARGET_DIR, f"{base}_{counter}{ext}")
                        counter += 1
                    
                    try:
                        shutil.move(src, dst)
                        print(f"  -> Moved completed file: {file}")
                    except Exception:
                        # File might still be downloading or locked by slskd
                        pass
    
    time.sleep(15)
