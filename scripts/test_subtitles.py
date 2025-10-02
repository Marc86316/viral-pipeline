# scripts/test_subtitles.py

import os
import sys
# 確保專案根目錄在 sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

import yt_dlp
from core.video_downloader import sanitize_filename
from core.subtitle_translate import download_subtitles, translate_subtitles

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=lknNsZgzG1g&t=712s"
    # 自動根據影片標題建立資料夾
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get("title", "video")
    safe_title = sanitize_filename(title)
    out_dir = os.path.join("data", safe_title)
    # 下載英文字幕
    vtt = download_subtitles(url, out_dir)
    print("Downloaded:", vtt)
    # 翻譯成繁中
    zh = translate_subtitles(vtt)
    print("Translated:", zh)