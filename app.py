from flask import Flask, request, render_template, redirect, url_for
import os
from utils.processing import process_input, process_url, process_json_file
from utils.ui import browse_recipes

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
    recipes_list = browse_recipes()  # This should now return a list of dictionaries.
    if not recipes_list:
        recipes_list = [{'title': 'No recipes found', 'picture_url': 'path/to/default/image.png'}]
    return render_template('recipes.html', recipes=recipes_list)

if __name__ == '__main__':
    app.run(debug=True)
