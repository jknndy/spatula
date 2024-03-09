import sys
from utils.ui import browse_recipes
from utils.processing import process_input


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "browse":
            browse_recipes()
        else:
            process_input(sys.argv[1])
    else:
        print("Usage: python main.py <recipe_url|file_path> or 'browse'")
