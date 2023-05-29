from flask import Flask, render_template, request
import csv
from math import ceil

app = Flask(__name__)

def read_recipe_data():
    recipes = []
    try:
        with open('recipes.csv', 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                recipes.append(row)
    except IOError:
        # Handle file reading error
        return None
    return recipes

def paginate_recipes(recipes, page_size, page_number):
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    return recipes[start_index:end_index]

@app.route('/')
def index():
    recipes = read_recipe_data()
    if recipes is None:
        # Handle error case
        return "Error: Failed to read recipe data"

    page = request.args.get('page', default=1, type=int)
    page_size = 20
    paginated_recipes = paginate_recipes(recipes, page_size, page)

    total_pages = ceil(len(recipes) / page_size)

    return render_template('index.html', recipes=paginated_recipes, page=page, total_pages=total_pages)

@app.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    recipes = read_recipe_data()
    if recipes is None:
        # Handle error case
        return "Error: Failed to read recipe data"
    if recipe_id >= 0 and recipe_id < len(recipes):
        recipe = recipes[recipe_id]
        return render_template('recipe.html', recipe=recipe)
    else:
        return "Recipe not found"

if __name__ == "__main__":
    app.run(debug=True)
