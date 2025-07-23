from pathlib import Path

# Base directory for your project
base_dir = Path("/Users/chenzhende/Documents/GitHub/viral-pipeline")

# Define required directories
dirs = [
    "core",
    "config",
    "utils",
    "data/subtitles",
    "data/comments",
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
    # ...（此處省略其餘檔案清單，同 init 腳本中完整內容）
}

# Create files with content
for rel_path, content in files.items():
    file_path = base_dir / rel_path
    if not file_path.exists():
        file_path.write_text(content, encoding="utf-8")
        print(f"Created: {file_path}")
    else:
        print(f"Skipped (exists): {file_path}")

print("\nProject skeleton generated at:", base_dir)