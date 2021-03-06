from requests import put, get, post
import json

#Inserting recipe
def test_recipe_inserts():
    payload =  {"_title": "Add_Recipe","recipe": {"name": "French Omelette","creator": "Incredible Egg","description": "This French omelette recipe is a classic and versatile favorite. Fill with cheese and ham or change it up by adding leftover cooked vegetables.","create_date": "2016-10-06","cooking_time": "420"},"ingredient": [{"name": "egg","description": "chicken egg","measurement": "2","unit": "whole"},{"name": "water","description": "cooking water","measurement": "2","unit": "teaspoon"},{"name": "salt","description": "","measurement": "0.125","unit": "teaspoon"},{"name": "pepper","description": "","measurement": "0.125","unit": "teaspoon"},{"name": "butter","description": "","measurement": "1","unit": "teaspoon"},{"name": "shredded cheese","description": "","measurement": "0.5","unit": "cup"},{"name": "chopped ham","description": "","measurement": "0.5","unit": "cup"}]}
    headers = {'Content-type': 'application/json'}
    r = post("http://localhost:5000/recipes/FrenchOmlette", data=json.dumps(payload), headers=headers)
    print r.text

    payload = {"_title": "Add_Recipe","recipe": {"name": "Fried Rice","creator": "The Recipe Critic","description": "A quick fried rice like you get at your favorite Chinese restaurant. A couple of eggs, baby carrots, peas and soy sauce is all you need.","create_date": "2014-05-10","cooking_time": "2100"},"ingredient": [{"name": "white rice","description": "","measurement": "2","unit": "cup"},{"name": "water","description": "","measurement": "4","unit": "cup"},{"name": "chopped baby carrots","description": "","measurement": "0.67","unit": "cup"},{"name": "onions","description": "","measurement": "0.5","unit": "cup"},{"name": "vegetable oil","description": "","measurement": "2","unit": "teaspoon"},{"name": "egg","description": "","measurement": "2","unit": "whole"},{"name": "soy sauce","description": "","measurement": "1","unit": "teaspoon"},{"name": "sesame oil","description": "","measurement": "1","unit": "teaspoon"}]}
    headers = {'Content-type': 'application/json'}
    r = post("http://localhost:5000/recipes/FriedRice", data=json.dumps(payload), headers=headers)
    print r.text

#Inserting Users
def test_user_inserts():
    payload =  {"_title": "Add_User","user": {"first_name" :"bob","last_name" : "smith","sex":"Male","address": "245 huge st San francisco  CA 94016 USA","phone":"2069221931","create_date":"2017-05-05 06:08:09"},"diet_preference": [{"ingredient":"pepper","create_date":"2017-05-05 06:08:09"},{"ingredient":"soy sauce","create_date":"2017-05-05 06:09:10"}]}
    headers = {'Content-type': 'application/json'}
    r = post("http://localhost:5000/user/4", data=json.dumps(payload), headers=headers)
    print r.text

def test_cookpref_inserts():
    payload = { "_title": "Add_Cooking_Preferrence","user_id": "4","cooking_preferrence": [{"recipe":"French Omelette","ingredient":"chopped ham","preferrence":"welldone"},{"recipe":"Fried Rice","ingredient":"onions","preferrence":"brown"}]}
    headers = {'Content-type': 'application/json'}
    r = post("http://localhost:5000/user/cookpref/4", data=json.dumps(payload), headers=headers)
    print r.text

if __name__ == '__main__':
    test_recipe_inserts()
