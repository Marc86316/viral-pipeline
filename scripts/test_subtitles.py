# scripts/test_subtitles.py

import os
import sys
# 確保專案根目錄在 sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

from core.subtitle_translate import download_subtitles, translate_subtitles

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=lqhAOtplWYA"
    out_dir = "data/5_Second_Countdown_HD"
    # 下載英文字幕
    vtt = download_subtitles(url, out_dir)
    print("Downloaded:", vtt)
    # 翻譯成繁中
    zh = translate_subtitles(vtt)
    print("Translated:", zh)