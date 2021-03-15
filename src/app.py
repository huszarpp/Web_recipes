from flask import Flask, render_template, request, redirect, url_for, session

from src.common.database import Database
from src.models.types_of_food import Types_Of_Food
from src.models.food import Food
from src.models.ingredients import Ingredients

app = Flask(__name__)
app.secret_key = "peter"


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/')
def root():
    return redirect(url_for('get_home'))


@app.route('/home')
def get_home():
    return render_template('home.html')


@app.route('/recipes', methods=['GET'])
def recipes():
    categories = Types_Of_Food.find_all_types()
    foods = Food.find_foods()
    return render_template('recipes.html', foods=foods, categories=categories)


@app.route('/recipes/category/<type_id>', methods=['GET'])
def get_recipes_by_category(type_id):
    category = Types_Of_Food.find_one_id(type_id)
    foods = Food.find_foods_by_type(type_id)
    return render_template('recipes_by_type.html', foods=foods, category=category)


@app.route('/recipes/name/<recipe_id>', methods=['GET'])
def get_recipes_by_id(recipe_id):
    food = Food.find_one_food_by_id(recipe_id)
    ingredients = Ingredients.find_ingredients_by_food_id(recipe_id)
    return render_template('recipes_by_id.html', recipe_id=recipe_id, food=food, ingredients=ingredients)

"""
@app.route('/recipes/name/<recipe_id>', methods=['DELETE'])
def del_recipe_by_id(recipe_id):
    Food.delete_food(recipe_id)
    Ingredients.delete_ingredient(recipe_id)
    return redirect(url_for('recipes'))
"""

@app.route('/recipes/name/test', methods=['DELETE'])
def del_recipe_by_id(recipe_id):
    # Food.delete_food(recipe_id)
    return render_template('test.html', food_id=recipe_id)


@app.route('/recipes/name', methods=['GET'])
def new_recipe():
    categories = Types_Of_Food.find_all_types()
    return render_template('recipes_new.html', categories=categories)


@app.route('/recipes/name/save', methods=['POST'])
def new_recipe_save():
    food_name = request.form['food_name']
    food_category = request.form['category']
    food_img = request.form['food_img']
    food_prep = request.form['food_prep']

    if Food.food_exists(food_name):
        return render_template('food_exists.html', name=food_name)

    if Types_Of_Food.type_exists(food_category):
        typef = Types_Of_Food.find_one_type(type=food_category)
        type_id = typef.get_id()
    else:
        typef = Types_Of_Food(type=food_category)
        typef.save_type()
        typef = Types_Of_Food.find_one_type(type=food_category)
        type_id = typef.get_id()

    food = Food(name=food_name, preparation=food_prep, type_id=type_id, img=food_img)
    food.save_food()

    food_id = food.get_id()

    return redirect(url_for('add_ingredient', food_id=food_id))


@app.route('/recipes/<food_id>/ingredient', methods=['GET'])
def add_ingredient(food_id):
    food = Food.find_one_food_by_id(food_id)
    food_name = food.name
    food_img = food.img
    food_type = Types_Of_Food.find_one_id(food.type_id)
    food_category = food_type.type
    food_prep = food.preparation

    ingredients_exist = Ingredients.find_ingredients_by_food_id(food.get_id())
    ingredients_all = Ingredients.find_all_ingredients()

    return render_template('add_ingredients.html', food_id=food_id, food_name=food_name, food_img=food_img,
                           food_category=food_category,
                           food_prep=food_prep, ingredients_all=ingredients_all, ingredients_exist=ingredients_exist)


@app.route('/recipes/name/<food_id>/ingredient', methods=['POST'])
def save_ingredient(food_id):
    ingredient_name = request.form['ing_name']
    quantity = request.form['ing_quant']
    unit = request.form['ing_unit']

    ingredient = Ingredients(ingredient=ingredient_name, quantity=quantity, unit=unit, food_id=food_id)
    ingredient.save_ingredient()

    return redirect(url_for('get_recipes_by_id', recipe_id=food_id)) if request.args.get(
        'redirectToFood') else redirect(url_for('add_ingredient', food_id=food_id))


if __name__ == '__main__':
    app.run()
