# YT_Downloader_Pro


![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange)

YouTube Downloader Pro is a Python-based desktop application that allows you to download YouTube videos or playlists in various formats (video or audio) and quality settings. It features a user-friendly graphical interface built with Tkinter and uses the `yt-dlp` library for downloading.

## Features

- **Download Videos or Playlists**: Supports downloading single videos or entire playlists.
- **Customizable Quality Settings**:
  - Video: 2160p, 1440p, 1080p, 720p, 480p, 360p.
  - Audio: 320k, 256k, 192k, 160k, 128k.
- **Progress Tracking**: Real-time progress bar and download status updates.
- **Output Directory Selection**: Choose where to save downloaded files.
- **Playlist Range Selection**: Download specific ranges of videos from a playlist.
- **Threaded Downloads**: Non-blocking UI during downloads.

## Installation

### Prerequisites

- Python 3.8 or higher.
- `yt-dlp` library.
- Tkinter (usually included with Python).

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hamawebdev/YT_Downloader_Pro
   cd YT_Downloader_Pro
   ```

2. **Install dependencies**:
   ```bash
    pip install yt-dlp ffmpeg-python
    sudo pacman -S ffmpeg tk
   ```

3. **Run the application**:
   ```bash
   python youtube_downloader.py
   ```

## Usage

1. **Enter YouTube URL**: Paste the URL of the video or playlist you want to download.
2. **Select Format**: Choose between `video` or `audio`.
3. **Set Quality**: Select the desired quality for the download.
4. **Choose Output Directory**: Specify where to save the downloaded files.
5. **Start Download**: Click the "Start Download" button to begin.

For playlists:
- Enable the "Download Playlist" checkbox.
- Specify the start and end video indices if you want to download a specific range.
