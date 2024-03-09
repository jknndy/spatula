import sys
import os
import json
from recipe_scrapers import scrape_me
import subprocess
import platform  # Import platform module

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

def setup_storage():
    config = load_config()
    if not config["storage_location"]:
        print("\033[91m\nFirst-time setup: Where would you like to store your recipes?\033[0m")
        print("\033[91mPress Enter to use the default location (./recipes/), or specify a new path.\033[0m")
        location = input().strip() or "./recipes/"
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

def clear_screen():
    if platform.system() == "Windows":
        subprocess.run(["cls"], check=True, shell=True)
    else:
        subprocess.run(["clear"], check=True)

def browse_recipes():
    storage_location = setup_storage()
    recipes = [f.replace('_', ' ').replace('.json', '') for f in os.listdir(storage_location) if f.endswith('.json')]
    print("\n".join(f"\033[96m{idx}. {recipe}\033[0m" for idx, recipe in enumerate(recipes, start=1)))
    while True:
        try:
            user_input = input("Select a recipe by number (or type 'exit' to quit): ").strip()
            if user_input.lower() == 'exit':
                print("Exiting.")
                return
            choice = int(user_input) - 1
            if 0 <= choice < len(recipes):
                clear_screen()
                filepath = os.path.join(storage_location, recipes[choice].replace(' ', '_') + '.json')
                with open(filepath, 'r') as f:
                    recipe_data = json.load(f)
                format_output(recipe_data)
                break
            else:
                print("\033[91mInvalid selection. Please enter a number from the list.\033[0m")
        except ValueError:
            print("\033[91mPlease enter a valid number.\033[0m")

def safe_access(callable_attr):
    try:
        return callable_attr()
    except Exception:
        return None

def scrape_recipe(url):
    try:
        scraper = scrape_me(url)
        return {
            "title": safe_access(scraper.title),
            "author": safe_access(scraper.author),
            "total_time": safe_access(scraper.total_time),
            "yields": safe_access(scraper.yields),
            "ingredients": safe_access(scraper.ingredients),
            "instructions": safe_access(lambda: scraper.instructions().split('\n')),
            "equipment": safe_access(scraper.equipment) if hasattr(scraper, 'equipment') else None
        }
    except Exception as e:
        return {"error": str(e)}

def format_output(data):
    if "error" in data:
        print("\033[91mError:\033[0m", data["error"])
        return

    print(f"\033[92m{data['title']}\033[0m")
    if data['author']:
        print(f"\033[96mby {data['author']}\033[0m")
    for key in ["total_time", "yields", "ingredients", "instructions", "equipment"]:
        value = data.get(key)
        if value:
            print(f"\033[96m{key.capitalize()}:\033[0m", end="")
            if isinstance(value, list):
                print("\n" + "\n".join(f"- {item}" for item in value))
            else:
                print(f" {value}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "browse":
            browse_recipes()
        else:
            recipe_data = scrape_recipe(sys.argv[1])
            format_output(recipe_data)
            save_recipe(recipe_data)
    else:
        print("Usage: python main.py <recipe_url> or 'browse'")
