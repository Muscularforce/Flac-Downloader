import os
import sys

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
# SLSKD API Configuration
# ---------------------------------------------------------------------------
# The URL where your local or remote slskd instance is accessible:
SLSKD_URL = os.environ.get("SLSKD_URL", "http://localhost:5030")

# Your slskd API key.
# Generate one in slskd Web UI: Options -> General -> API Keys
API_KEY = os.environ.get("SLSKD_API_KEY", "YOUR_API_KEY_HERE")

def get_headers():
    return {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }

def validate_config():
    """Validates that the user has configured an API key."""
    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        print("=" * 65)
        print("[!] ERROR: slskd API Key is not configured.")
        print("=" * 65)
        print("Please configure your API key by doing ONE of the following:")
        print("  1. Open 'config.py' and set API_KEY = 'your_key_here'")
        print("  2. Create a '.env' file with: SLSKD_API_KEY=your_key_here")
        print("  3. Set the environment variable: SLSKD_API_KEY=your_key_here")
        print("\nHow to get a key:")
        print("  Open your slskd Web UI (http://localhost:5030)")
        print("  Go to: Options -> General -> API Keys and generate one.")
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
