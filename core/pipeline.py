"""
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
