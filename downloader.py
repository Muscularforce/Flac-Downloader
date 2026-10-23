import os
import time
import requests

# Configuration for slskd
SLSKD_URL = "http://localhost:5030"
API_KEY = "antigravity1234567890"  # Automatically added via slskd configuration

def get_headers():
    return {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }

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
    print(f"Searching for: {query}")
    url = f"{SLSKD_URL}/api/v0/searches"
    data = {"searchText": query}
    
    try:
        response = requests.post(url, json=data, headers=get_headers())
        if response.status_code != 200:
            print(f"Error starting search: {response.text}")
            return None
        
        search_id = response.json().get("id")
        print(f"Search started with ID: {search_id}")
        return search_id
    except requests.exceptions.ConnectionError:
        print("Could not connect to slskd. Is it running?")
        exit(1)

def poll_search_results(search_id, timeout_secs=90):
    print("Waiting for results...")
    url = f"{SLSKD_URL}/api/v0/searches/{search_id}"
    
    start_time = time.time()
    
    # Priority order for file extensions
    preferred_exts = [".flac", ".wav", ".mp3", ".m4a"]
    best_file = None
    best_username = None
    best_ext_index = 999
    
    while time.time() - start_time < timeout_secs:
        responses_url = f"{url}/responses"
        response = requests.get(responses_url, headers=get_headers())
        print(f"Poll {time.time() - start_time:.1f}s: status={response.status_code}")
        if response.status_code == 200:
            responses_data = response.json()
            print(f"Fetched {len(responses_data)} responses from API.")
            
            for res in responses_data:
                username = res.get("username")
                for file_info in res.get("files", []):
                    filename = file_info.get("filename", "").lower()
                    
                    for i, ext in enumerate(preferred_exts):
                        if filename.endswith(ext):
                            if i < best_ext_index:
                                best_ext_index = i
                                best_file = file_info
                                best_username = username
                            break
                            
            # If we found a FLAC (index 0), just return it immediately to save time
            if best_ext_index == 0:
                print(f"Found FLAC file immediately: {best_file.get('filename')}")
                return best_username, best_file
                        
        time.sleep(2)
        
    # Return whatever best file we found after the timeout (WAV, MP3, etc.)
    return best_username, best_file

def download_file(username, file_info):
    filename = file_info.get("filename")
    print(f"Initiating download for: {filename} from {username}")
    
    url = f"{SLSKD_URL}/api/v0/transfers/downloads/{username}"
    
    # Payload requires the filename and size
    payload = [{
        "filename": filename,
        "size": file_info.get("size")
    }]
    
    response = requests.post(url, json=payload, headers=get_headers())
    if response.status_code in (200, 201, 202):
        print("Download queued successfully!")
    else:
        print(f"Failed to queue download: {response.status_code} - {response.text}")

if __name__ == "__main__":
    playlist_file = "playlist.txt" 
    
    if not os.path.exists(playlist_file):
        print(f"Please create a '{playlist_file}' with one song per line.")
        # Create a dummy one for the user
        with open(playlist_file, 'w') as f:
            f.write("# Add your songs here (Artist - Title)\n")
        print(f"I created an empty '{playlist_file}' for you.")
        exit(1)
        
    songs = read_playlist(playlist_file)
    if not songs:
        print(f"'{playlist_file}' is empty. Add some songs and run again.")
        exit(1)
        
    for song in songs:
        search_id = search_song(song)
        if search_id:
            username, file_info = poll_search_results(search_id)
            if username and file_info:
                print(f"Found match: {file_info.get('filename')} ({file_info.get('size')} bytes)")
                download_file(username, file_info)
            else:
                print(f"Could not find any high quality file for: {song} within the timeout.")
        
        print("-" * 40)
        time.sleep(1) # small delay between searches
