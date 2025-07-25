"""
Orchestrate the end-to-end MVP pipeline.
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import argparse

def run_mvp(video_url: str, config_path: str = "config/settings.yaml"):
    from core.video_downloader import download_and_rename_video
    from config.config import DEEPL_API_KEY
    result = download_and_rename_video(video_url, DEEPL_API_KEY)
    print("Downloaded and saved to:", result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run viral-pipeline MVP")
    parser.add_argument("url", help="YouTube video or Short URL")
    parser.add_argument("--config", default="config/settings.yaml", help="Path to settings file")
    args = parser.parse_args()
    run_mvp(args.url, args.config)
    sys.exit(0)