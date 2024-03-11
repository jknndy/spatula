from pathlib import Path
import json
from typing import Union

from utils.scraping import scrape_recipe, KEY_ALIASES
from utils.ui import format_output
from utils.storage import save_recipe

def process_input(input_value: str) -> None:
    try:
        input_path = Path(input_value)
        if input_path.is_file():
            if input_path.suffix == '.json':
                process_json_file(input_path)
            elif input_path.suffix == '.txt':
                process_txt_file(input_path)
            else:
                print(f"Unsupported file type: {input_path.suffix}")
        else:
            process_url(input_value)
    except Exception as e:
        print(f"Error: {e}")

def process_url(url: str, print_output: bool = True) -> None:
    recipe_data = scrape_recipe(url)
    format_output(recipe_data, print_output=print_output)
    save_recipe(recipe_data)

def process_txt_file(file_path: Union[str, Path]) -> None:
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = [url.strip() for url in file if url.strip()]
        for url in urls:
            process_url(url, print_output=False)

def process_json_file(file_path: Union[str, Path]) -> None:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            recipes = json.load(file)
        recipes = [recipes] if isinstance(recipes, dict) else recipes
        for recipe_data in recipes:
            mapped_recipe_data = {KEY_ALIASES.get(k, k): v for k, v in recipe_data.items()}
            format_output(mapped_recipe_data)
            save_recipe(mapped_recipe_data)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error processing JSON file: {e}")
