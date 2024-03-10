import sys
from utils.ui import browse_recipes
from utils.processing import process_input
from utils.ui import clear_screen, format_output, get_recipe_by_filename

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "browse":
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
        else:
            process_input(sys.argv[1])
    else:
        print("Usage: python main.py <recipe_url|file_path> or 'browse'")
