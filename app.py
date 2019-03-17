from flask import Flask, url_for, redirect, render_template, request
import json
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "recipe-manager"
app.config["MONGO_URI"] = "mongodb://root:adg37tup@ds133496.mlab.com:33496/recipe-manager"

mongo = PyMongo(app)

######## Helper functions

# helper fuction which checks if allergens are present in the form data
def containsAllergens(formDict):
    if "containsAllergens" in formDict:
        # return true if there is allergens
        return True
    else:
        # otherwise return false
        return False


# helper function which grabs a dict value and returns a list of dict key-value pairs
def listifyDict(dictVal):
    listDict = []
    if "\r\n" in dictVal:
        # if there are new lines, split it and assign to a list variable
        listVal = dictVal.split("\r\n")

        # go through the split list and create a list of key-value pairs and return the list
        for item in listVal:
            listDict.append({"list_item": item})

        return listDict
    else:
        # otherwise return a single key-value pair
        return [{"list_item": dictVal}]


######## Recipes

# method to handle the '/' route or home page
@app.route("/")
def index():
    # fetch all recipes
    _recipes = mongo.db.recipes.find()

    # return the home page template html, and assign it a pagetitle and send accross the 'pageTitle'
    return render_template("recipes.html", pageTitle="Recipes", recipes=_recipes)


# method to handle the 'add-recipe' page
@app.route("/add-recipe")
def addRecipe():
    allCategories = mongo.db.categories.find()
    return render_template("add-recipe.html", pageTitle="Add Recipe", categories=allCategories)


# method to handle the adding of a new recipe to the database
@app.route("/insert-recipe", methods=["POST"])
def insertRecipe():
    # convert form data into a dictionary
    formData = request.form.to_dict()

    # check and see if form data contains allergens
    hasAllergens = containsAllergens(formData)

    # break up ingredients & recipe steps into a list
    if "\r\n" in formData["recipe_ingredients"] or "\r\n" in formData["recipe_steps"]:
        formData["recipe_ingredients"] = listifyDict(formData["recipe_ingredients"])
        formData["recipe_steps"] = listifyDict(formData["recipe_steps"])

    if hasAllergens == True:
        # if there are allergens then set the 'containsAllergens' key to a value of 'True'
        formData["containsAllergens"] = True
    else:
        formData["containsAllergens"] = False
        print(formData)
    
    # add recipe_views to dict
    formData["recipe_views"] = 0

    # add a new recipe to database
    mongo.db.recipes.insert_one(formData)

    # then perform a re-direct to the home page
    return redirect(url_for("index"))


# run app in debugging mode
app.run(debug=True)