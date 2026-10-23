import os
import shutil
import time

source_dir = r"C:\Users\Jovan Fernandes\AppData\Local\slskd\downloads"
target_dir = r"C:\Users\Jovan Fernandes\Desktop\AkamoPlaylist"

print("Starting background watch to move completed songs...")
while True:
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
                
                try:
                    shutil.move(src, dst)
                    print(f"Moved {file}")
                except Exception as e:
                    # Ignore errors, file might be still downloading and locked by slskd
                    pass
    
    time.sleep(30)
