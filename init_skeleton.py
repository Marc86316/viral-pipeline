OVERWRITE = False  # Set to False if you want to preserve existing files
from pathlib import Path

# Base directory for your project
base_dir = Path("/Users/chenzhende/Documents/GitHub/viral-pipeline")

# Define required directories
dirs = [
    "core",
    "config",
    "utils",
    "data",  # Only create the base data folder; per-video folders will be created dynamically
    "output",
    "templates",
    "assets"
]

# Create directories
for d in dirs:
    (base_dir / d).mkdir(parents=True, exist_ok=True)

# Define skeleton files and their initial contents
files = {
    "core/video_downloader.py": '''"""
Download YouTube videos and fetch metadata.
"""
def download_video(url: str) -> str:
    """Download video and return filepath."""
    pass

def get_video_title(url: str) -> str:
    """Fetch video title without downloading content."""
    pass
''',
    "core/subtitle_translate.py": '''"""
Download and translate subtitles using DeepL; track usage.
"""
def download_subtitles(video_url: str, out_dir: str) -> str:
    """Download subtitles to out_dir and return filepath."""
    pass

def translate_subtitles(vtt_path: str, target_lang: str) -> str:
    """Translate VTT at vtt_path into target_lang, return new filepath."""
    pass

def get_deepl_usage() -> dict:
    """Query DeepL usage and return statistics."""
    pass
''',
    "core/nlp_embeddings.py": '''"""
Embed comments into vector representations.
"""
def embed_comments(texts):
    """Return embedding array for list of comment texts."""
    pass
''',
    "core/subtitle_embedding.py": '''"""
Parse and embed subtitle segments.
"""
def parse_vtt(vtt_path: str):
    """Return list of (timestamp, text) from VTT file."""
    pass

def embed_subtitles(segments):
    """Return embedding array for subtitle text segments."""
    pass
''',
    "core/comment_pairing.py": '''"""
Match subtitle embeddings to comment embeddings.
"""
def pair_comments(sub_emb, comm_emb, threshold=0.7):
    """
    Return list of {timestamp, comment, score} for comment insertion.
    """
    pass
''',
    "core/blender_embed.py": '''"""
Use Blender Python API to overlay comments in video.
"""
def insert_comments_in_video(video_path: str, comment_schedule, output_path: str):
    """Insert comment overlays into video using Blender scripting."""
    pass
''',
    "core/pipeline.py": '''"""
Orchestrate the end-to-end MVP pipeline.
"""
def run_mvp(video_url: str, config_path: str = "config/settings.yaml"):
    """Execute full pipeline: download, subtitle, embedding, pairing, rendering."""
    pass

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run viral-pipeline MVP")
    parser.add_argument("url", help="YouTube video or Short URL")
    parser.add_argument("--config", default="config/settings.yaml", help="Path to settings file")
    args = parser.parse_args()
    run_mvp(args.url, args.config)
''',
    "config/settings.yaml": '''# API keys and other configuration
yt_api_key: YOUR_YOUTUBE_API_KEY_HERE
deepl_api_key: YOUR_DEEPL_API_KEY_HERE
''',
    "utils/logger.py": '''"""
Logging configuration for viral-pipeline.
"""
import logging

def setup_logger(name=__name__):
    """Create and return a logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
''',
    "requirements.txt": '''yt-dlp
requests
google-api-python-client
deepl
''',
    "README.md": '''# viral-pipeline

An automated pipeline for downloading YouTube videos/Shorts, extracting and translating subtitles, fetching top comments, embedding NLP matching, and assembling final content for social media reposting.

## Folder Structure

```
viral-pipeline/
├── core/                     # Source code
├── config/                   # API keys and settings
├── utils/                    # Logger or utility functions
├── data/                     # Contains subfolders per video title
│   └── {video_title}/        # Folder per video
│       ├── video.mp4         # Downloaded video
│       ├── subtitles_zh.vtt  # Translated subtitles
│       └── comments.json     # Extracted top comments
├── output/                   # Final rendered video (optional)
├── templates/                # Text or overlay templates
└── assets/                   # Static images/fonts for rendering

## Quickstart
'''
}


# Create files with content
for rel_path, content in files.items():
    file_path = base_dir / rel_path
    if OVERWRITE or not file_path.exists():
        file_path.write_text(content, encoding="utf-8")
        print(f"{'Overwritten' if file_path.exists() else 'Created'}: {file_path}")
    else:
        print(f"Skipped (exists): {file_path}")

print("\nProject skeleton generated at:", base_dir)