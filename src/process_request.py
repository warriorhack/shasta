#!flask/bin/python
#Author: Chiraag

import json
from DB import DB

class Process_Request(object):
    def __init__(self):
        self.recipe_name = None
        self.recipe = None
        self.parser = None
        self.conn_str = None
        self.Dbobj = None
        self.user_details = None
        self.user_id = None
        self.cook_details = None
        self.ingredient = None

    def set_config(self, conn_str):
        self.conn_str = conn_str

    def getRecipe(self, recipe_name):
        self.recipe_name = recipe_name
        self.Dbobj = DB(self.conn_str)
        self.Dbobj.connect()
        query = "SELECT name, creator,description,cooking_time FROM recipe WHERE isactive is True and name = '%s'"%(self.recipe_name)
        rows = self.Dbobj.run_select_query(query)
        return rows

    def postRecipe(self, recipe):

        self.recipe = recipe
        #Create an DB object
        self.Dbobj = DB(self.conn_str)
        #parse the payload
        if "recipe" in self.recipe:
            recipe_obj = None
            recipe_obj = self.recipe["recipe"]
            recipe_name = recipe_obj["name"]
            creator = recipe_obj["creator"]
            description = recipe_obj["description"]
            create_date = recipe_obj["create_date"]
            cooking_time = recipe_obj["cooking_time"]
        if "ingredient" in self.recipe:
            ingredients = self.recipe["ingredient"]
            for ingredient in ingredients:
                ing_name = ingredient["name"]
                ing_description = ingredient["description"]
                ing_measurement = ingredient["measurement"]
                ing_unit = ingredient["unit"]
                db_data = (recipe_name,creator,description,create_date,cooking_time,ing_name,ing_description,ing_measurement,ing_unit)
                self.Dbobj.connect()
                out = None
                out = self.Dbobj.call_proc('sp_insert_recipe', db_data)
                self.Dbobj.disconnect()
                if not out:
                    return {"Found":"Issue"}

        return {"Worked":"Well"}

    def getUser(self, user_id):
        self.user_id = user_id
        self.Dbobj = DB(self.conn_str)
        self.Dbobj.connect()
        query = "SELECT first_name, last_name,sex,address,phone, id as user_id FROM users WHERE isactive is True and id = %s"%(self.user_id)
        rows = self.Dbobj.run_select_query(query)
        return rows

    def postUser(self,user_details):
        self.user_details = user_details

        self.Dbobj = DB(self.conn_str)
        if "user" in self.user_details:
            user_obj = None
            user_obj = self.user_details["user"]
            first_name = user_obj["first_name"]
            last_name = user_obj["last_name"]
            sex = user_obj["sex"]
            address = user_obj["address"]
            phone = user_obj["phone"]
            user_create_date = user_obj["create_date"]
        if "diet_preference" in self.user_details:
            diet_preferences = self.user_details["diet_preference"]
            for diet_preference in diet_preferences:
                ingredient = diet_preference["ingredient"]
                ing_create_date = diet_preference["create_date"]
                db_data = (first_name,last_name,sex,address,phone,user_create_date,ingredient,ing_create_date)
                self.Dbobj.connect()
                out = None
                out = self.Dbobj.call_proc('sp_insert_user', db_data)
                self.Dbobj.disconnect()
                if not out:
                    return {"Found":"Issue"}
        return {"Worked":"Well"}

    def getCookPref(self, user_id):
        self.user_id = user_id
        self.Dbobj = DB(self.conn_str)
        self.Dbobj.connect()
        query = "SELECT r.name as recipe, i.name as ingredient, cp.preferrence from cooking_preferrence_map cpm inner join cooking_preferrence cp on cpm.preferrence_id = cp.id inner join recipe r on r.id = cpm.recipe_id inner join ingredient i on i.id = cpm.ingredient_id where cpm.user_id = %s and r.isactive is True"%(self.user_id)
        rows = self.Dbobj.run_select_query(query)
        return rows

    def postCookPref(self, cook_details):
        self.cook_details = cook_details

        self.Dbobj = DB(self.conn_str)
        if "user_id" in self.cook_details:
            user_id = self.cook_details["user_id"]
        if "cooking_preferrence" in self.cook_details:
            cooking_preferrences = self.cook_details["cooking_preferrence"]
            for cooking_preferrence in cooking_preferrences:
                recipe = cooking_preferrence["recipe"]
                ingredient = cooking_preferrence["ingredient"]
                preferrence = cooking_preferrence["preferrence"]
                db_data = (user_id,recipe,ingredient,preferrence)
                self.Dbobj.connect()
                out = None
                out = self.Dbobj.call_proc('sp_insert_cookpref', db_data)
                self.Dbobj.disconnect()
                if not out:
                    return {"Found":"Issue"}
        return {"Worked":"Well"}

    def getAllRecipes(self):
        self.Dbobj = DB(self.conn_str)
        self.Dbobj.connect()
        query = """SELECT name, creator,description,cooking_time FROM recipe WHERE isactive is True"""
        rows = self.Dbobj.run_select_query(query)
        return rows


    def listRecipes(self):
        self.Dbobj = DB(self.conn_str)
        self.Dbobj.connect()
        query = """SELECT name, creator FROM recipe WHERE isactive is True"""
        rows = self.Dbobj.run_select_query(query)
        return rows

    def getDietPreference(self, user_id):
        self.user_id = user_id
        self.Dbobj = DB(self.conn_str)
        self.Dbobj.connect()
        query = "SELECT i.name as ingredient FROM user_diet_preference_map cdm inner join ingredient i on i.id = cdm.ingredient_id where cdm.isactive = True and cdm.user_id = %s"%(self.user_id)
        rows = self.Dbobj.run_select_query(query)
        return rows

    def getRecipesByIngredient(self, ingredient):
        self.ingredient = ingredient
        self.Dbobj = DB(self.conn_str)
        self.Dbobj.connect()
        query = "SELECT r.name as recipe, r.creator as creator, r.description as description FROM recipe_ingredient_map rim inner join recipe r on r.id = rim.recipe_id inner join ingredient i on i.id = rim.ingredient_id where r.isactive = True and i.name = '%s'"%(self.ingredient)
        rows = self.Dbobj.run_select_query(query)
        return rows

    def getIngredientForRecipe(self, recipe_name):
        self.recipe_name = recipe_name
        self.Dbobj = DB(self.conn_str)
        self.Dbobj.connect()
        query = "SELECT i.name as ingredient, CAST(m.measurement AS TEXT) as measurement, m.unit as unit from recipe_ingredient_map rim inner join recipe r on r.id = rim.recipe_id inner join ingredient i on i.id = rim.ingredient_id inner join measurements m on m.id = rim.measurements_id where r.name = '%s'"%(self.recipe_name)
        rows = self.Dbobj.run_select_query(query)
        return rows

    def getRecipesDietPref(self, user_id):
        self.user_id = user_id
        self.Dbobj = DB(self.conn_str)
        self.Dbobj.connect()
        query = "todo"
        rows = self.Dbobj.run_select_query(query)
        return rows
