# 🎧 Soulseek FLAC Downloader

An automated Python tool to batch download lossless FLAC music from the Soulseek network via the [slskd](https://github.com/slskd/slskd) client REST API.

---

## ✨ Features

- **FLAC Priority**: Searches the Soulseek P2P network and automatically selects lossless `.flac` files first (falls back to `.wav`, `.mp3`, or `.m4a` if FLAC is unavailable).
- **Playlist Automation**: Just paste your tracklist in `playlist.txt` (`Artist - Title`) and run!
- **Zero-Config Auto Login**: Automatically logs into slskd using default credentials — no manual API key generation needed!
- **Batch Processing**: Automatically queues searches, handles timeouts, and adds downloads to `slskd`.
- **Auto Organizer**: Automatically moves completed audio files into your designated playlist directory (e.g., Desktop or Music folder).
- **One-Click Windows Launchers**: Double-click `.bat` files for instant running without command line experience.

---

## 📋 Prerequisites

1. **Python 3.8+** installed: [Download Python](https://www.python.org/downloads/)  
   *(Make sure to check **"Add Python to PATH"** during installation)*
2. **slskd** running on your computer: [Download slskd Releases](https://github.com/slskd/slskd/releases)  
   - Run `slskd.exe` (accessible by default at `http://localhost:5030`).
   - Log into the slskd Web UI *(Default Web UI login: `slskd` / `slskd`)*.
   - **No API key setup is required!** The downloader logs in automatically using default slskd credentials.

---

## ⚡ Quick Start

### 1. Install Dependencies
Double-click `install_requirements.bat`, or run:
```bash
pip install -r requirements.txt
```

### 2. Add Songs to Download
Open `playlist.txt` and add your songs (one per line):
```text
Imagine Dragons - Bones
Sia - Unstoppable
Alan Walker - Spectre
```

### 3. Run!
- **Standard Downloader**: Double-click `run_downloader.bat` (or run `python downloader.py`).
- **Batch Download & Move**: Double-click `run_batch_runner.bat` (or run `python batch_runner.py`) — this queues all songs, waits for downloads to finish, and moves them into your `Desktop/AkamoPlaylist` folder!

---

## ⚙️ Configuration (Optional)

By default, **zero configuration is needed** — it works out of the box with any standard slskd installation!

If you want to customize settings, open `config.py` (or `.env`):

| Setting | Default Value | Description |
| :--- | :--- | :--- |
| `SLSKD_URL` | `http://localhost:5030` | Address of your slskd server |
| `SLSKD_USERNAME` | `slskd` | Your slskd Web UI username |
| `SLSKD_PASSWORD` | `slskd` | Your slskd Web UI password |
| `API_KEY` | *(empty)* | Optional API key if configured in `slskd.yml` |
| `SOURCE_DIR` | `%LOCALAPPDATA%\slskd\downloads` | Directory where slskd writes completed downloads |
| `TARGET_DIR` | `Desktop/AkamoPlaylist` | Directory where songs are moved after completion |

---

## 🛠️ Scripts Overview

| File | Purpose |
| :--- | :--- |
| `downloader.py` | Searches Soulseek for each song in `playlist.txt` and queues the best FLAC match into slskd. |
| `batch_runner.py` | Runs `downloader.py`, monitors download progress, and moves completed audio files to your target folder. |
| `watch_and_move.py` | Background watcher daemon that continuously moves finished tracks as soon as slskd finishes them. |
| `move_songs.py` | One-shot utility to move any audio files from slskd's downloads folder to your target folder. |
| `test_search.py` | Simple utility script to test your slskd connection and verify API functionality. |

---

## 📄 License

MIT License. Free for personal and open-source use.
