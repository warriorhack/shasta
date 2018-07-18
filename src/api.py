#!flask/bin/python

from flask import Flask, request
from flask_restful import Resource, Api
from process_request import Process_Request

app = Flask(__name__)
app.config.from_envvar('CONFIG', silent=True)
api = Api(app)

recipe = {}

#Return details
class Recipe(Resource):
    #Search for a recipe
    def get(self, recipe_name):
        process = Process_Request()
        process.set_config(app.config['DATABASE_CONN_STRING'])
        return process.getRecipe(recipe_name)

    def post(self, recipe_name):
        payload = request.get_json()
        process = Process_Request()
        process.set_config(app.config['DATABASE_CONN_STRING'])
        return process.postRecipe(payload)

class ListDietPreference(Resource):

    def get(self, user_id):
        process = Process_Request()
        process.set_config(app.config['DATABASE_CONN_STRING'])
        return process.getDietPreference(user_id)

class GetIngredientForRecipe(Resource):
    #Search for a recipe
    def get(self, recipe_name):
        process = Process_Request()
        process.set_config(app.config['DATABASE_CONN_STRING'])
        return process.getIngredientForRecipe(recipe_name)

class GetRecipesDietPref(Resource):
    def get(self, user_id):
        process = Process_Request()
        process.set_config(app.config['DATABASE_CONN_STRING'])
        return process.getRecipesDietPref()

class GetAllRecipes(Resource):

    def get(self):
        process = Process_Request()
        process.set_config(app.config['DATABASE_CONN_STRING'])
        return process.getAllRecipes()

class GetRecipesByIngredient(Resource):

    def get(self, ingredient_name):
        process = Process_Request()
        process.set_config(app.config['DATABASE_CONN_STRING'])
        return process.getRecipesByIngredient(ingredient_name)

# List all the recipes
class ListRecipes(Resource):

    def get(self):
        process = Process_Request()
        process.set_config(app.config['DATABASE_CONN_STRING'])
        return process.listRecipes()

#Add a new user
class User(Resource):

    def get(self, user_id):
        process = Process_Request()
        process.set_config(app.config['DATABASE_CONN_STRING'])
        return process.getUser(user_id)

    def post(self, user_id):
        payload = request.get_json()
        process = Process_Request()
        process.set_config(app.config['DATABASE_CONN_STRING'])
        return process.postUser(payload)

class Cooking_Preferrence(Resource):

    def get(self, user_id):
        process = Process_Request()
        process.set_config(app.config['DATABASE_CONN_STRING'])
        return process.getCookPref(user_id)

    def post(self, user_id):
        payload = request.get_json()
        process = Process_Request()
        process.set_config(app.config['DATABASE_CONN_STRING'])
        return process.postCookPref(payload)

api.add_resource(Recipe,'/recipes/<string:recipe_name>')
api.add_resource(GetAllRecipes,'/recipes/all')
api.add_resource(ListRecipes,'/recipes/list')
api.add_resource(GetRecipesByIngredient, '/recipes/ingredient/<string:ingredient_name>')
api.add_resource(GetIngredientForRecipe, '/ingredient/recipes/<string:recipe_name>')
api.add_resource(GetRecipesDietPref, '/recipes/dietpref/<int:user_id>')
api.add_resource(User,'/user/<int:user_id>')
api.add_resource(Cooking_Preferrence,'/user/cookpref/<int:user_id>')
api.add_resource(ListDietPreference, '/user/dietpref/<int:user_id>')


if __name__ == '__main__':
    app.run()
