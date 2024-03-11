import json
import subprocess
import platform
from pathlib import Path
from typing import List, Dict, Optional

from utils.storage import setup_storage

def clear_screen() -> None:
    command = "cls" if platform.system() == "Windows" else "clear"
    subprocess.run([command], check=True, shell=True)

def format_output(data: Dict[str, Optional[str]], print_output: bool = True) -> None:
    if "error" in data:
        print("\033[91mError:\033[0m", data["error"])
        return

    if print_output:
        print(f"\033[92m{data.get('title', 'Unknown Recipe')}\033[0m")
        author = data.get('author')
        if author:
            print(f"\033[96mby {author}\033[0m")
        for key in ["total_time", "cook_time", "prep_time", "yields", "ingredients", "instructions", "equipment"]:
            value = data.get(key)
            if value:
                print(f"\033[96m{key.capitalize()}:\033[0m", end="")
                if isinstance(value, list):
                    print("\n" + "\n".join(f"- {item}" for item in value))
                else:
                    print(f" {value}")

def browse_recipes() -> List[Dict[str, str]]:
    storage_location = Path(setup_storage())
    recipe_files = list(storage_location.glob('*.json'))
    recipes_list = []

    for filepath in recipe_files:
        with open(filepath, 'r') as file:
            recipe = json.load(file)
            recipe['filename'] = filepath.name
            recipes_list.append(recipe)

    recipes_list.sort(key=lambda x: x.get('created_at', '0'), reverse=True)

    adjusted_recipes_list = [{
        'title': recipe.get('title', recipe['filename'].replace('_', ' ').replace('.json', '')),
        'picture': recipe.get('picture', 'https://via.placeholder.com/150'),
        'site_name': recipe.get('site_name', ''),
        'filename': recipe['filename']
    } for recipe in recipes_list]

    return adjusted_recipes_list

def get_recipe_by_filename(filename: str) -> Optional[Dict[str, str]]:
    storage_location = Path(setup_storage())
    filepath = storage_location / f"{filename}.json"
    if filepath.exists():
        return json.loads(filepath.read_text())
    else:
        print(f"Recipe file not found: {filename}.json")
        return None
