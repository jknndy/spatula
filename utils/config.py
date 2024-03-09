import json

config_file = "config.json"

def load_config():
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"storage_location": ""}

def save_config(config):
    with open(config_file, 'w') as f:
        json.dump(config, f)
