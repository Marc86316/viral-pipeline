# viral-pipeline
An automated pipeline for downloading YouTube Shorts/videos, extracting subtitles and top comments, translating titles/subtitles, and preparing content for social media reposting.

## License

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License**.  
See the [LICENSE](./LICENSE) file for details.

```text
viral-pipeline/
├── core/
│   ├── video_downloader.py         # download video & extract title
│   ├── subtitle_translate.py       # download & translate subtitles, track DeepL usage
│   ├── nlp_embeddings.py           # existing comment embedding prototype
│   ├── subtitle_embedding.py       # embed subtitles into vectors
│   ├── comment_pairing.py          # match subtitle vectors ↔ comment vectors, find insert timestamps
│   ├── blender_embed.py            # insert comments into video via Blender scripting
│   └── pipeline.py                 # orchestrate end-to-end MVP flow
├── config/
│   └── settings.yaml               # API keys, thresholds, paths
├── data/
│   ├── subtitles/                  # raw & translated VTTs
│   ├── comments/                   # raw & filtered comment text
│   └── embeddings/                 # serialized vectors
└── utils/
    └── logger.py                   # logging setup
```

### Output Parameters

The following outputs are returned from `video_downloader.py` functions:

| Function                            | Return Variable     | Type   | Description                                                                 |
|-------------------------------------|----------------------|--------|-----------------------------------------------------------------------------|
| `download_video(url)`              | `filename`           | `str`  | Downloaded video filename (e.g., `abc123.mp4`)                              |
| `get_video_title(url)`             | `title`              | `str`  | Original video title from YouTube                                           |
| `sanitize_filename(text)`          | `sanitized_text`     | `str`  | Cleaned title with symbols removed and underscores applied                  |
| `translate_to_english(text, key)`  | `translated_text`    | `str`  | English translation of the video title using DeepL                          |
| `download_and_rename_video(url, key)` | `dict`             | `dict` | Output includes original, translated title and final sanitized filename     |

Example return from `download_and_rename_video()`:
```python
{
    "original_title": "原始標題（可能為非英文）",
    "translated_title": "English Title",
    "final_filename": "English_Title.mp4"
}
```