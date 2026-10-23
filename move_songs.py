import os
import shutil

source_dir = r"C:\Users\Jovan Fernandes\AppData\Local\slskd\downloads"
target_dir = r"C:\Users\Jovan Fernandes\Desktop\AkamoPlaylist"

print(f"Moving files from {source_dir} to {target_dir}")
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
            
            try:
                shutil.move(src, dst)
                moved_count += 1
                print(f"Moved {file}")
            except Exception as e:
                print(f"Could not move {file}: {e}")

print(f"Successfully moved {moved_count} songs to {target_dir}")
