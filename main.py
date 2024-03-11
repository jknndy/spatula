import argparse
from utils.ui import browse_recipes, clear_screen, format_output, get_recipe_by_filename
from utils.processing import process_input

def browse():
    recipes = browse_recipes()
    for index, recipe in enumerate(recipes, start=1):
        print(f"{index}. {recipe['title']}")
    try:
        choice = int(input("Select a recipe number to view details: ")) - 1
        if 0 <= choice < len(recipes):
            selected_recipe = recipes[choice]
            recipe_details = get_recipe_by_filename(selected_recipe['filename'].replace('.json', ''))
            clear_screen()
            format_output(recipe_details)
        else:
            print("Invalid selection. Please run the command again and select a valid number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def main(url_or_path: str):
    process_input(url_or_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recipe Management System")
    parser.add_argument('action', nargs='?', help="Specify 'browse' to view recipes or a URL/file path to process a new recipe.", default='browse')
    args = parser.parse_args()

    if args.action.lower() == 'browse':
        browse()
    else:
        main(args.action)
