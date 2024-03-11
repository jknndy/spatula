from flask import Flask, request, render_template, make_response
from pathlib import Path
from utils.processing import process_input
from utils.ui import browse_recipes, get_recipe_by_filename
import os

app = Flask(__name__)

@app.route('/')
def home():
    recent_recipes = browse_recipes()[:4]
    return render_template('home.html', recent_recipes=recent_recipes)

@app.route('/process', methods=['POST'])
def process():
    input_value = request.form.get('input_value')
    if input_value:
        try:
            input_path = Path(input_value)
            if input_path.is_file() or input_value.startswith("http"):
                process_input(input_value)
                message = "Processing completed successfully."
            else:
                message = "Invalid input. Please provide a valid file path or URL."
        except Exception as e:
            message = f"An error occurred: {str(e)}"
    else:
        message = "No input provided. Please enter a URL or file path."

    return render_template('process.html', message=message)

@app.route('/recipes')
def recipes():
    recipes_list = browse_recipes()
    if not recipes_list:
        recipes_list = [{'title': 'No recipes found', 'picture': 'https://via.placeholder.com/150', 'site_name': ''}]
    site_names = sorted(set(recipe['site_name'] for recipe in recipes_list if recipe.get('site_name')))
    return render_template('recipes.html', recipes=recipes_list, site_names=site_names)

@app.route('/recipe/<filename>')
def recipe_detail(filename):
    recipe = get_recipe_by_filename(filename)
    if recipe:
        return render_template('recipe_detail.html', recipe=recipe)
    else:
        response = make_response("Recipe not found", 404)
        return response

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', False))
