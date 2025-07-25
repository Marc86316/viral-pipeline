# config.py

import yaml
from pathlib import Path

# 找到同一資料夾裡的 settings.yaml
_config_path = Path(__file__).parent / "settings.yaml"

try:
    with open(_config_path, "r", encoding="utf-8") as f:
        _config = yaml.safe_load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"Cannot find configuration file: {_config_path}")

# 將 YAML 裡的欄位取出成為模組變數
DEEPL_API_KEY = _config.get("deepl_api_key")
YT_API_KEY    = _config.get("yt_api_key")