# Soulseek Playlist Downloader

This is a Python script that automates downloading a list of songs in FLAC format from Soulseek. It interacts with the [slskd](https://github.com/slskd/slskd) client via its REST API.

## Prerequisites

1. **Python 3.x** needs to be installed (https://www.python.org/downloads/).
2. **slskd** running on your PC. `slskd` is a modern headless Soulseek client that provides the API we need to talk to the network.
   * Download and run `slskd` from [here](https://github.com/slskd/slskd/releases).
   * Once it is running (usually accessible at `http://localhost:5030`), go to its Web UI.
   * Log in with your Soulseek credentials.
   *(Default username and password are both **slskd**)*
   * Go to **Options -> General -> API Keys** and generate a new API key.

## Setup

1. Open `downloader.py` in an editor.
2. Look for the line `API_KEY = "YOUR_API_KEY_HERE"` and paste the API key you generated in `slskd` there.
3. Open a terminal in this folder and install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## How to use

1. Add your songs to the `playlist.txt` file (one song per line). It's best to use the format `Artist Name - Song Name` for better search results.
2. Run the script:
   ```bash
   python downloader.py
   ```

The script will search for each song, wait for results, look for the first `.flac` file it can find, and tell `slskd` to download it. The downloaded files will appear in whatever download directory you configured in your `slskd` settings!
