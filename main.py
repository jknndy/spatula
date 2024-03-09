import sys
import os
import json
from recipe_scrapers import scrape_me

config_file = "config.json"

def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        return {"storage_location": ""}

def save_config(config):
    with open(config_file, 'w') as f:
        json.dump(config, f)

def setup_storage():
    config = load_config()
    if not config["storage_location"]:
        red_start = "\033[91m"
        red_end = "\033[0m"
        
        print(f"{red_start}\nFirst-time setup: Where would you like to store your recipes?{red_end}")
        print(f"{red_start}Press Enter to use the default location (./recipes/), or specify a new path.{red_end}")
        location = input().strip() or "./recipes/"
        config["storage_location"] = location
        save_config(config)
        if not os.path.exists(location):
            os.makedirs(location)
    return config["storage_location"]

def save_recipe(data):
    storage_location = setup_storage()
    filename = f"{data['title'].replace(' ', '_')}.json"
    filepath = os.path.join(storage_location, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f)
    print(f"Recipe saved to {filepath}")

def browse_recipes():
    storage_location = setup_storage()
    recipes = [f.replace('_', ' ').replace('.json', '') for f in os.listdir(storage_location) if f.endswith('.json')]
    for idx, recipe in enumerate(recipes, start=1):
        print(f"{idx}. {recipe}")
    choice = int(input("Select a recipe by number: ")) - 1
    if 0 <= choice < len(recipes):
        with open(os.path.join(storage_location, recipes[choice].replace(' ', '_') + '.json'), 'r') as f:
            recipe_data = json.load(f)
        format_output(recipe_data)
    else:
        print("Invalid selection.")

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

def print_header(header, newline=True):
    if newline:
        print(f"\n\033[96m{header}:\033[0m", end=' ')
    else:
        print(f"\033[96m{header}:\033[0m", end=' ')

def format_output(data):
    if "error" in data:
        print("Error:", data["error"])
        return

    print(f"\n{data['title']}")
    if data['author']:
        print(data['author'])

    for key in ["total_time", "yields", "ingredients", "instructions", "equipment"]:
        value = data[key]
        if value:
            print_header(key.capitalize(), newline=True if key != "author" else False)
            if isinstance(value, list):
                print('')
                for item in value:
                    print(f"- {item}")
            else:
                print(f"\n{value}")

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
