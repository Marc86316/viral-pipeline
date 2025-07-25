"""
Download YouTube videos and fetch metadata.
"""

import yt_dlp
import json
import requests
import re
from pathlib import Path
import os
import shutil

def download_video(url: str) -> str:
    """Download video and return filepath."""
    ydl_opts = {
        'format': 'bestvideo+bestaudio',
        'merge_output_format': 'mp4',
        'outtmpl': '%(id)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = f"{info['id']}.mp4"
        return filename

def get_video_title(url: str) -> str:
    """Fetch video title without downloading content."""
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['title']

def sanitize_filename(text: str) -> str:
    text = re.sub(r"[^\w\s\u4e00-\u9fff-]", "", text)  # keep En, Ch
    return text.strip().replace(" ", "_")

def translate_to_english(text: str, deepl_api_key: str) -> str:
    response = requests.post(
        "https://api-free.deepl.com/v2/translate",
        data={
            "auth_key": deepl_api_key,
            "text": text,
            "target_lang": "EN"
        }
    )
    response.raise_for_status()
    return response.json()["translations"][0]["text"]

def download_and_rename_video(video_url: str, deepl_api_key: str):
    ydl_opts = {
        'format': 'bestvideo+bestaudio',
        'merge_output_format': 'mp4',
        'writeinfojson': True,
        'outtmpl': '%(id)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        video_id = info_dict['id']

    info_path = Path(f"{video_id}.info.json")
    if not info_path.exists():
        raise FileNotFoundError("can't find file info.json, process might be failed")

    with open(info_path, encoding="utf-8") as f:
        info = json.load(f)
        original_title = info["title"]

    translated_title = translate_to_english(original_title, deepl_api_key)
    safe_title = sanitize_filename(translated_title)

    # Create target directory under data/
    target_dir = Path("data") / safe_title
    target_dir.mkdir(parents=True, exist_ok=True)

    # Move video file
    mp4_path = Path(f"{video_id}.mp4")
    if mp4_path.exists():
        final_video_path = target_dir / f"{safe_title}.mp4"
        mp4_path.rename(final_video_path)

    # Move info JSON
    if info_path.exists():
        final_info_path = target_dir / f"{safe_title}.info.json"
        info_path.rename(final_info_path)

    return {
        "original_title": original_title,
        "translated_title": translated_title,
        "final_filename": str(final_video_path),
        "target_directory": str(target_dir)
    }
