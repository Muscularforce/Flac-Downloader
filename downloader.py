import os
import sys
import time
import requests
from config import SLSKD_URL, get_headers, PREFERRED_EXTENSIONS, validate_config

def read_playlist(file_path):
    songs = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Ignore empty lines and comments
            if line and not line.startswith('#'):
                songs.append(line)
    return songs

def search_song(query):
    print(f"\n🔍 Searching for: {query}")
    url = f"{SLSKD_URL}/api/v0/searches"
    data = {"searchText": query}
    
    try:
        response = requests.post(url, json=data, headers=get_headers())
        if response.status_code != 200:
            print(f"❌ Error starting search: {response.text}")
            return None
        
        search_id = response.json().get("id")
        print(f"📡 Search started (ID: {search_id})")
        return search_id
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to slskd. Make sure slskd is running (default: http://localhost:5030).")
        sys.exit(1)

def poll_search_results(search_id, timeout_secs=90):
    print("⏳ Waiting for peer responses...")
    url = f"{SLSKD_URL}/api/v0/searches/{search_id}"
    
    start_time = time.time()
    
    best_file = None
    best_username = None
    best_ext_index = 999
    
    while time.time() - start_time < timeout_secs:
        responses_url = f"{url}/responses"
        try:
            response = requests.get(responses_url, headers=get_headers())
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error polling responses: {e}")
            time.sleep(2)
            continue

        if response.status_code == 200:
            responses_data = response.json()
            
            for res in responses_data:
                username = res.get("username")
                for file_info in res.get("files", []):
                    filename = file_info.get("filename", "").lower()
                    
                    for i, ext in enumerate(PREFERRED_EXTENSIONS):
                        if filename.endswith(ext):
                            if i < best_ext_index:
                                best_ext_index = i
                                best_file = file_info
                                best_username = username
                            break
                            
            # If we found a FLAC file (index 0), queue it immediately to save time
            if best_ext_index == 0:
                print(f"✨ Found FLAC file immediately: {best_file.get('filename')}")
                return best_username, best_file
                        
        time.sleep(2)
        
    # Return whatever best file we found after timeout (WAV, MP3, etc.)
    return best_username, best_file

def download_file(username, file_info):
    filename = file_info.get("filename")
    size_mb = file_info.get("size", 0) / (1024 * 1024)
    print(f"⬇️  Queuing download: {filename} ({size_mb:.2f} MB) from user '{username}'")
    
    url = f"{SLSKD_URL}/api/v0/transfers/downloads/{username}"
    
    # Payload requires filename and size
    payload = [{
        "filename": filename,
        "size": file_info.get("size")
    }]
    
    try:
        response = requests.post(url, json=payload, headers=get_headers())
        if response.status_code in (200, 201, 202):
            print("✅ Download queued successfully in slskd!")
        else:
            print(f"❌ Failed to queue download ({response.status_code}): {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error communicating with slskd transfer API: {e}")

if __name__ == "__main__":
    validate_config()

    playlist_file = "playlist.txt" 
    
    if not os.path.exists(playlist_file):
        print(f"File '{playlist_file}' not found.")
        with open(playlist_file, 'w', encoding='utf-8') as f:
            f.write("# Add your songs here (Artist - Title)\n")
        print(f"Created a starter '{playlist_file}' for you.")
        sys.exit(1)
        
    songs = read_playlist(playlist_file)
    if not songs:
        print(f"'{playlist_file}' is empty. Please add songs and run again.")
        sys.exit(1)
        
    print(f"🎵 Found {len(songs)} song(s) in playlist.")
    for idx, song in enumerate(songs, 1):
        print(f"\n[{idx}/{len(songs)}] ----------------------------------------")
        search_id = search_song(song)
        if search_id:
            username, file_info = poll_search_results(search_id)
            if username and file_info:
                download_file(username, file_info)
            else:
                print(f"⚠️  Could not find any suitable audio file for: {song} within timeout.")
        
        time.sleep(1) # Grace period between searches

    print("\n🎉 All playlist items processed!")
