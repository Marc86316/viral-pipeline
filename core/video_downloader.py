
"""
Download YouTube videos and fetch metadata.
"""

import yt_dlp
import json
import requests
import re
from pathlib import Path

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
    text = re.sub(r"[^\w\s\u4e00-\u9fff-]", "", text)  # 保留中英文、數字
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
        raise FileNotFoundError("找不到 info.json，下載階段可能失敗")

    with open(info_path, encoding="utf-8") as f:
        info = json.load(f)
        original_title = info["title"]

    translated_title = translate_to_english(original_title, deepl_api_key)
    safe_title = sanitize_filename(translated_title)

    mp4_path = Path(f"{video_id}.mp4")
    if mp4_path.exists():
        mp4_path.rename(f"{safe_title}.mp4")
    if info_path.exists():
        info_path.rename(f"{safe_title}.info.json")

    return {
        "original_title": original_title,
        "translated_title": translated_title,
        "final_filename": f"{safe_title}.mp4"
    }