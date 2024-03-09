import os
import json
from utils.config import load_config, save_config

def setup_storage():
    config = load_config()
    if not config["storage_location"]:
        location = input("\033[91m\nFirst-time setup: Where would you like to store your recipes?\033[0m\n\033[91mPress Enter to use the default location (./recipes/), or specify a new path.\033[0m\n").strip() or "./recipes/"
        config["storage_location"] = location
        save_config(config)
    os.makedirs(config["storage_location"], exist_ok=True)
    return config["storage_location"]

def save_recipe(data):
    storage_location = setup_storage()
    filename = f"{data['title'].replace(' ', '_')}.json"
    filepath = os.path.join(storage_location, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f)
    print(f"\033[92mRecipe saved to {filepath}\033[0m")
