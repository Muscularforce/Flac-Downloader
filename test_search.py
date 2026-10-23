import time
import requests
from config import SLSKD_URL, get_headers, validate_config

validate_config()

print("🔍 Testing connection to slskd API...")
url = f"{SLSKD_URL}/api/v0/searches"
data = {"searchText": "Imagine Dragons - Believer"}

try:
    response = requests.post(url, json=data, headers=get_headers())
    if response.status_code != 200:
        print(f"❌ API error: {response.text}")
        exit(1)
        
    search_id = response.json().get("id")
    print(f"📡 Search started successfully with ID: {search_id}")
    print("⏳ Waiting 5 seconds for results...")
    time.sleep(5)

    responses_url = f"{url}/{search_id}/responses"
    response = requests.get(responses_url, headers=get_headers())
    responses_data = response.json()
    print(f"✅ Fetched {len(responses_data)} peer response(s)")

    flac_count = 0
    for res in responses_data:
        for file_info in res.get("files", []):
            filename = file_info.get("filename", "").lower()
            if filename.endswith(".flac"):
                flac_count += 1
                if flac_count == 1:
                    print(f"✨ Example FLAC found: {file_info.get('filename')}")

    print(f"📊 Total FLAC files found: {flac_count}")
    print("🎉 SLSKD connection and search test passed!")
except requests.exceptions.ConnectionError:
    print("❌ Could not connect to slskd. Please check that slskd is running at", SLSKD_URL)
