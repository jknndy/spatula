import os
import subprocess
import platform
import json
from utils.storage import setup_storage

def clear_screen():
    if platform.system() == "Windows":
        subprocess.run(["cls"], check=True, shell=True)
    else:
        subprocess.run(["clear"], check=True)

def format_output(data, print_output=True):
    if "error" in data:
        print("\033[91mError:\033[0m", data["error"])
        return

    if print_output:
        print(f"\033[92m{data['title']}\033[0m")
        if data.get('author'):
            print(f"\033[96mby {data['author']}\033[0m")
        for key in ["total_time", "cook_time", "prep_time", "yields", "ingredients", "instructions", "equipment"]:
            value = data.get(key)
            if value:
                print(f"\033[96m{key.capitalize()}:\033[0m", end="")
                if isinstance(value, list):
                    print("\n" + "\n".join(f"- {item}" for item in value))
                else:
                    print(f" {value}")

def browse_recipes():
    storage_location = setup_storage()
    recipe_files = [f for f in os.listdir(storage_location) if f.endswith('.json')]
    recipes_list = []

    for filename in recipe_files:
        filepath = os.path.join(storage_location, filename)
        with open(filepath, 'r') as file:
            recipe = json.load(file)
            recipes_list.append({
                'title': recipe.get('title', filename.replace('_', ' ').replace('.json', '')),
                'picture': recipe.get('picture', 'https://via.placeholder.com/150')  # Use 'picture' as the key
            })

    return recipes_list

def get_recipe_by_filename(filename):
    storage_location = "./recipes"  # Adjust this path to where your recipes are stored
    filepath = os.path.join(storage_location, filename + '.json')
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)
    else:
        return None