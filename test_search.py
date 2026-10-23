import requests, time, json

SLSKD_URL = "http://localhost:5030"
API_KEY = "antigravity1234567890"

def get_headers():
    return {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }

print("Starting search...")
url = f"{SLSKD_URL}/api/v0/searches"
data = {"searchText": "Imagine Dragons - Believer"}
response = requests.post(url, json=data, headers=get_headers())
search_id = response.json().get("id")
print(f"Search ID: {search_id}")

time.sleep(5)
responses_url = f"{url}/{search_id}/responses"
response = requests.get(responses_url, headers=get_headers())

responses_data = response.json()
print(f"Fetched {len(responses_data)} responses")

flac_files = []
for res in responses_data:
    for file_info in res.get("files", []):
        filename = file_info.get("filename", "").lower()
        if filename.endswith(".flac"):
            flac_files.append(filename)

print(f"Found {len(flac_files)} flac files.")
if flac_files:
    print("Example:", flac_files[0])
