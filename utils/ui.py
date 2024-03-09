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
    recipes = [f.replace('_', ' ').replace('.json', '') for f in os.listdir(storage_location) if f.endswith('.json')]
    print("\n".join(f"\033[96m{idx}. {recipe}\033[0m" for idx, recipe in enumerate(recipes, start=1)))
    while True:
        user_input = input("Select a recipe by number (or type 'exit' to quit): ").strip()
        if user_input.lower() == 'exit':
            print("Exiting.")
            return
        try:
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
