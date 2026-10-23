import os
import sys
import requests

# ---------------------------------------------------------------------------
# Helper: Simple .env parser (without requiring external python-dotenv)
# ---------------------------------------------------------------------------
def _load_env_file():
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_file):
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, val = line.split("=", 1)
                        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))
        except Exception:
            pass

_load_env_file()

# ---------------------------------------------------------------------------
# SLSKD Connection & Authentication Configuration
# ---------------------------------------------------------------------------
# Address where your local or remote slskd instance is running:
SLSKD_URL = os.environ.get("SLSKD_URL", "http://localhost:5030")

# Method 1 (Auto-Login, Recommended): Default slskd Web UI Credentials
# Every new slskd install defaults to "slskd" / "slskd". If you didn't change
# them, you don't have to touch anything — it works out of the box!
SLSKD_USERNAME = os.environ.get("SLSKD_USERNAME", "slskd")
SLSKD_PASSWORD = os.environ.get("SLSKD_PASSWORD", "slskd")

# Method 2 (Optional): API Key
# If you configured an API key in slskd.yml, you can specify it here:
API_KEY = os.environ.get("SLSKD_API_KEY", "")

_cached_token = None

def get_headers():
    global _cached_token

    # 1. If a custom API key is configured, use it:
    if API_KEY and API_KEY not in ("YOUR_API_KEY_HERE", ""):
        return {
            "X-Api-Key": API_KEY,
            "Content-Type": "application/json"
        }

    # 2. If we already obtained a session Bearer token, reuse it:
    if _cached_token:
        return {
            "Authorization": f"Bearer {_cached_token}",
            "Content-Type": "application/json"
        }

    # 3. Otherwise, automatically log in via session endpoint using username & password:
    try:
        session_url = f"{SLSKD_URL}/api/v0/session"
        res = requests.post(
            session_url,
            json={"username": SLSKD_USERNAME, "password": SLSKD_PASSWORD},
            timeout=5
        )
        if res.status_code == 200:
            token = res.json().get("token")
            if token:
                _cached_token = token
                return {
                    "Authorization": f"Bearer {_cached_token}",
                    "Content-Type": "application/json"
                }
    except Exception:
        pass

    # 4. Fallback for unauthenticated instances
    return {
        "Content-Type": "application/json"
    }

def validate_config():
    """Validates connectivity and authentication with slskd before starting."""
    try:
        test_url = f"{SLSKD_URL}/api/v0/application"
        res = requests.get(test_url, headers=get_headers(), timeout=5)
        if res.status_code in (200, 204):
            return True
        elif res.status_code in (401, 403):
            print("=" * 65)
            print("[!] Authentication Failed for slskd")
            print("=" * 65)
            print("Could not log in to slskd automatically.")
            print("Default login is username: 'slskd', password: 'slskd'.")
            print("If you changed your credentials, update them in 'config.py':")
            print("  - SLSKD_USERNAME = 'your_username'")
            print("  - SLSKD_PASSWORD = 'your_password'")
            print("Or set your API key in 'config.py':")
            print("  - API_KEY = 'your_api_key'")
            print("=" * 65)
            sys.exit(1)
        else:
            print(f"[!] Notice: slskd returned HTTP {res.status_code}")
    except requests.exceptions.ConnectionError:
        print("=" * 65)
        print("[!] Cannot connect to slskd")
        print("=" * 65)
        print(f"Could not connect to slskd at: {SLSKD_URL}")
        print("Please make sure slskd is running (e.g., launch slskd.exe).")
        print("=" * 65)
        sys.exit(1)

# ---------------------------------------------------------------------------
# Directory Paths
# ---------------------------------------------------------------------------
# On Windows, slskd default downloads directory is in %LOCALAPPDATA%\slskd\downloads.
_local_appdata = os.environ.get("LOCALAPPDATA", os.path.expanduser("~"))
DEFAULT_SOURCE_DIR = os.path.join(_local_appdata, "slskd", "downloads")
SOURCE_DIR = os.environ.get("SLSKD_DOWNLOADS_DIR", DEFAULT_SOURCE_DIR)

# Destination directory where completed songs are organized/moved.
# Defaults to your Desktop/AkamoPlaylist.
_user_home = os.environ.get("USERPROFILE", os.path.expanduser("~"))
DEFAULT_TARGET_DIR = os.path.join(_user_home, "Desktop", "AkamoPlaylist")
TARGET_DIR = os.environ.get("TARGET_PLAYLIST_DIR", DEFAULT_TARGET_DIR)

# ---------------------------------------------------------------------------
# Preferred Audio Formats (in order of priority)
# ---------------------------------------------------------------------------
PREFERRED_EXTENSIONS = [".flac", ".wav", ".mp3", ".m4a"]
