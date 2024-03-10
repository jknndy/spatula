import os
import json
import datetime
from utils.config import load_config, save_config
from utils.scraping import KEY_ALIASES

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
    filename = f"{data.get('title', data.get('name', 'Recipe')).replace(' ', '_')}.json"
    filepath = os.path.join(storage_location, filename)
    keys_to_save = ["title", "name", "author", "source", "prep_time", "cook_time", "total_time", "duration", "yields", "servings", "ingredients", "instructions", "directions", "image", "canonical_url", "category", "site_name", "equipment"]
    data_to_save = {"created_at": datetime.datetime.now().isoformat()}
    for original_key in keys_to_save:
        if original_key in data:
            correct_key = KEY_ALIASES.get(original_key, original_key)
            data_to_save[correct_key] = data[original_key]

    with open(filepath, 'w') as f:
        json.dump(data_to_save, f, indent=4)

    print(f"\033[92mRecipe saved to {filepath}\033[0m")
