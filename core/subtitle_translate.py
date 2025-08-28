import requests
import yt_dlp
import csv
import json
from datetime import datetime
from pathlib import Path
from config.config import DEEPL_API_KEY
from core.video_downloader import sanitize_filename

def _split_text(text: str, chunk_size: int = 5000):
    """Helper to split long text into manageable chunks for DeepL."""
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

def download_subtitles(video_url: str, out_dir: str) -> str:
    """
    Download English subtitles (or auto-generated) for a YouTube video and save as VTT.
    Returns the filepath of the downloaded VTT.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # First, get metadata without downloading to obtain id and title
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl_meta:
        info = ydl_meta.extract_info(video_url, download=False)
        video_id = info['id']
        original_title = info.get('title', video_id)

    safe_title = sanitize_filename(original_title)

    # Download subtitles only (english preferred; fall back to auto)
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'outtmpl': str(out_dir / '%(id)s.%(ext)s'),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(video_url, download=True)

    # Locate the downloaded VTT (handle en and en-* variants)
    candidate = out_dir / f"{video_id}.en.vtt"
    if not candidate.exists():
        # fallback to any en-* variant
        matches = list(out_dir.glob(f"{video_id}.en*.vtt"))
        if matches:
            candidate = matches[0]
    if not candidate.exists():
        raise FileNotFoundError(
            f"No English (or auto) subtitles were found for this video. Tried: {video_id}.en.vtt and en-* variants in {out_dir}"
        )

    final_vtt = out_dir / f"EN_{safe_title}.vtt"
    candidate.rename(final_vtt)

    # Return the new path
    return str(final_vtt)

def translate_subtitles(vtt_path: str, target_lang: str = 'ZH-TW') -> str:
    """
    Translate a VTT subtitle file to the target language using DeepL.
    Returns the filepath of the translated VTT.
    """
    # Record usage before translation
    usage_before = get_deepl_usage()['character_count']
    vtt_path = Path(vtt_path)
    lines = vtt_path.read_text(encoding='utf-8').splitlines()
    output_lines = []
    buffer = []

    def _flush_buffer():
        if not buffer:
            return
        text_block = '\n'.join(buffer)
        translated_block = []
        for chunk in _split_text(text_block):
            resp = requests.post(
                "https://api-free.deepl.com/v2/translate",
                data={'auth_key': DEEPL_API_KEY, 'text': chunk, 'target_lang': target_lang}
            )
            resp.raise_for_status()
            translated_block.append(resp.json()['translations'][0]['text'])
        output_lines.extend('\n'.join(translated_block).splitlines())
        buffer.clear()

    for line in lines:
        # Preserve headers, timestamps, sequence numbers
        if line.startswith('WEBVTT') or '-->' in line or line.strip().isdigit() or not line.strip():
            _flush_buffer()
            output_lines.append(line)
        else:
            buffer.append(line)

    _flush_buffer()

    translated_path = vtt_path.parent / f"{vtt_path.stem}_{target_lang}.vtt"
    Path(translated_path).write_text('\n'.join(output_lines), encoding='utf-8')
    # Rename translated file to include sanitized title
    report_dir = vtt_path.parent
    # Extract video title from existing VTT name if needed
    safe_title = sanitize_filename(report_dir.name)
    final_translated = report_dir / f"ZH-TW_{safe_title}.vtt"
    Path(translated_path).rename(final_translated)
    # Record usage after translation
    usage_data = get_deepl_usage()
    usage_after = usage_data['character_count']
    limit = usage_data.get('character_limit', None)
    remaining = limit - usage_after if limit is not None else None
    consumed = max(0, usage_after - usage_before)
    timestamp = datetime.utcnow().isoformat() + 'Z'
    report_file = Path(__file__).parent.parent / 'deepl_usage_report.csv'
    is_new = not report_file.exists()
    with open(report_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(['timestamp', 'video_title', 'consumed_chars', 'total_used', 'char_limit', 'remaining'])
        writer.writerow([timestamp, safe_title, consumed, usage_after, limit, remaining])
    return str(final_translated)

def get_deepl_usage() -> dict:
    """
    Return current DeepL usage statistics.
    """
    resp = requests.get(
        "https://api-free.deepl.com/v2/usage",
        headers={"Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"}
    )
    resp.raise_for_status()
    return resp.json()
