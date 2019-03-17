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


#************ Recipes ************#

# method to handle the '/' route or home page
@app.route("/")
def index():
    # fetch all recipes
    _recipes = mongo.db.recipes.find()

    # return the home page template html, and assign it a pagetitle and send accross the 'pageTitle'
    return render_template("recipes.html", pageTitle="Recipes", recipes=_recipes)

######## Add a Recipe

# method to handle the 'add-recipe' page
@app.route("/add-recipe")
def addRecipe():
    # grab Categories from DB
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


######## View a Recipe

# method to handle the viewing of a single recipe
@app.route("/view-recipe/<recipe_id>")
def viewRecipe(recipe_id):
    recipeDB = mongo.db.recipes
    # Grab recipe entry
    recipeID = {"_id": ObjectId(recipe_id)}
    _recipe = mongo.db.recipes.find_one(recipeID)
    
    # each time a recipe is viewed increment the 'recipe_views' field
    currentViews = _recipe["recipe_views"]
    recipeDB.update_one(recipeID, {"$set": {"recipe_views": int(currentViews) + 1}})

    return render_template("view-recipe.html", pageTitle="View Recipe", recipe=_recipe)


######## Edit a Recipe

@app.route("/edit-recipe/<recipe_id>")
def editRecipe(recipe_id):
    # fetch entry for selected Recipe
    _recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})

    _ingr = _recipe["recipe_ingredients"]
    _steps = _recipe["recipe_steps"]

    # break up the ingredients & recipe steps into a new list for better handling on front-end
    listIngre = ["\r" + item["list_item"] for item in _ingr]
    listSteps = ["\r" + item["list_item"] for item in _steps]
    
    # grab Categories from DB
    allCategories = mongo.db.categories.find()

    return render_template("edit-recipe.html", recipe=_recipe, categories=allCategories, ingredients=listIngre, recipeSteps=listSteps)


@app.route("/update-recipe/<recipe_id>", methods=["POST"])
def updateRecipe(recipe_id):
    recipes = mongo.db["recipes"]

    # convert form data into a dictionary
    formData = request.form.to_dict()

    # used to target the entry we want to update
    queryId = {"_id": ObjectId(recipe_id)}

    # check and see if form data contains allergens
    hasAllergens = containsAllergens(formData)

    # grabbing the new values from the form submission and using them to create a dictionary
    if hasAllergens == True:
        # there are allergens, so make sure to include it in dict
        updatedValues = {
            "category_name": formData["category_name"],
            "recipe_title": formData["recipe_title"],
            "recipe_author": formData["recipe_author"],
            "recipe_description": formData["recipe_description"],
            "recipe_duration": formData["recipe_duration"],
            "recipe_ingredients": listifyDict(formData["recipe_ingredients"]),
            "containsAllergens": True,
            "recipe_allergens": formData["recipe_allergens"],
            "recipe_steps": listifyDict(formData["recipe_steps"])
        }
    else:
        # there is no allergens so Remove the recipe_allergens field from the Recipe entry
        recipes.update_one(queryId, {"$unset": {"recipe_allergens": 1}})

        # dict with updated values for recipe
        updatedValues = {
            "category_name": formData["category_name"],
            "recipe_title": formData["recipe_title"],
            "recipe_author": formData["recipe_author"],
            "recipe_description": formData["recipe_description"],
            "recipe_duration": formData["recipe_duration"],
            "recipe_ingredients": listifyDict(formData["recipe_ingredients"]),
            "containsAllergens": False,
            "recipe_steps": listifyDict(formData["recipe_steps"])
        }
    
    # Update the Recipe entry in the MongoDB database
    recipes.update_one(queryId, {"$set": updatedValues})

    # Re-direct to home page
    return redirect(url_for("index"))


######## Delete a Recipe

# remove recipe handler
@app.route("/delete-recipe/<recipe_id>")
def deleteRecipe(recipe_id):
    recipes = mongo.db["recipes"]

    # Delete the Recipe entry in the MongoDB database
    recipes.delete_one({"_id": ObjectId(recipe_id)})

    # Re-direct to home page
    return redirect(url_for("index"))


# run app in debugging mode
app.run(debug=True)