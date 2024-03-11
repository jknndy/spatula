import json
from pathlib import Path
from typing import Dict

config_file = Path("config.json")

def load_config() -> Dict[str, str]:
    try:
        return json.loads(config_file.read_text())
    except FileNotFoundError:
        return {"storage_location": ""}

def save_config(config: Dict[str, str]) -> None:
    config_file.write_text(json.dumps(config, indent=4))
