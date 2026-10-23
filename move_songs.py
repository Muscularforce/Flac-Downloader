import os
import shutil
from config import SOURCE_DIR, TARGET_DIR, PREFERRED_EXTENSIONS

print("=" * 60)
print("🚚 FLAC Downloader — Move Completed Songs")
print(f"📁 From: {SOURCE_DIR}")
print(f"🎯 To  : {TARGET_DIR}")
print("=" * 60)

os.makedirs(TARGET_DIR, exist_ok=True)
moved_count = 0

if not os.path.exists(SOURCE_DIR):
    print(f"⚠️ Source directory does not exist yet: {SOURCE_DIR}")
    exit(0)

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
                moved_count += 1
                print(f"  -> Moved: {file}")
            except Exception as e:
                print(f"  -> Could not move {file}: {e}")

print(f"\n🎉 Successfully moved {moved_count} song(s) to '{TARGET_DIR}'.")
