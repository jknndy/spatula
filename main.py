import sys
import os
import json
from utils.scraping import scrape_recipe, KEY_ALIASES
from utils.ui import browse_recipes, format_output
from utils.storage import save_recipe

def process_input(input_value):
    try:
        if os.path.isfile(input_value):
            process_json_file(input_value)
        else:
            process_url(input_value)
    except Exception as e:
        print(f"Error: {e}")

def process_url(url, print_output=True):
    recipe_data = scrape_recipe(url)
    format_output(recipe_data, print_output=print_output)
    save_recipe(recipe_data)

def process_txt_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
        for url in urls:
            url = url.strip()
            if url:
                process_url(url, print_output=False)

def process_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            recipes = json.load(file)
            if isinstance(recipes, dict):
                recipes = [recipes]
            for recipe_data in recipes:
                mapped_recipe_data = {KEY_ALIASES.get(k, k): v for k, v in recipe_data.items()}
                format_output(mapped_recipe_data)
                save_recipe(mapped_recipe_data)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error processing JSON file: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "browse":
            browse_recipes()
        else:
            process_input(sys.argv[1])
    else:
        print("Usage: python main.py <recipe_url|file_path> or 'browse'")
