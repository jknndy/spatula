from flask import Flask, request, render_template, redirect, url_for
import os
from utils.processing import process_input, process_json_file
from utils.ui import browse_recipes, get_recipe_by_filename

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/process', methods=['POST'])
def process():
    input_value = request.form.get('input_value')
    if input_value:
        try:
            if os.path.isfile(input_value) or input_value.startswith("http"):
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
        recipes_list = [{'title': 'No recipes found', 'picture': ''}]
    return render_template('recipes.html', recipes=recipes_list)

@app.route('/recipe/<filename>')
def recipe_detail(filename):
    recipe = get_recipe_by_filename(filename)
    if recipe:
        return render_template('recipe_detail.html', recipe=recipe)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)
