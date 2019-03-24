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
        # return true if the 'containsAllergens' property is present in the form submission data
        return True
    else:
        # no 'containsAllergens' property present in form data so return false
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
        # otherwise return a single key-value pair, with value being the parameter being passed to this function
        return [{"list_item": dictVal}]


#************ Recipes ************#

# method to handle the '/' route or home page
@app.route("/")
def index():
    # fetch all recipes
    _recipes = mongo.db.recipes.find()

    # grab Recipe count - this will be used on the front end to check if any recipes exist.
    # if no recipes exist in database, then a helpful message will be displayed in the front end.
    _recipeCount = mongo.db.recipes.count_documents({})

    # fetch categories for the Filter Recipe section on Home page
    allCategories = mongo.db.categories.find()

    # return the home page template html, and assign it a pagetitle and send accross the 'pageTitle'
    return render_template("recipes.html", pageTitle="Recipe Manager - Home", recipes=_recipes, recipeCount=_recipeCount, categories=allCategories)


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

    # break up ingredients & recipe steps into a list
    formData["recipe_ingredients"] = listifyDict(formData["recipe_ingredients"])
    formData["recipe_steps"] = listifyDict(formData["recipe_steps"])

    # check and see if form data contains 'containsAllergens' entry
    hasAllergensEntryInForm = containsAllergens(formData)

    if hasAllergensEntryInForm == True:
        # if there are allergens entry in form data then set the 'containsAllergens' key to a value of 'True'
        formData["containsAllergens"] = True
    else:
        # otherwise set it to 'False'
        formData["containsAllergens"] = False
    
    # add recipe_views key and an initial value of '0' to formData dict
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
    _recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    
    # each time a recipe is viewed increment the 'recipe_views' field
    currentViews = _recipe["recipe_views"]
    recipeDB.update_one({"_id": ObjectId(recipe_id)}, {"$set": {"recipe_views": int(currentViews) + 1}})

    return render_template("view-recipe.html", pageTitle="View Recipe", recipe=_recipe)


######## Edit a Recipe

# method to handle the editing of a recipe
@app.route("/edit-recipe/<recipe_id>")
def editRecipe(recipe_id):
    # fetch entry for selected Recipe
    _recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})

    # grab ingredient and steps entries of recipe
    ingrVal = _recipe["recipe_ingredients"]
    stepsVal = _recipe["recipe_steps"]

    # break up the ingredients & recipe steps into a new list for better handling on front-end.
    # A carriage return (\r) is pre-fixed to each list entry, so as to avoid unwanted spaces on the front-end
    ingreList = ["\r" + item["list_item"] for item in ingrVal]
    stepsList = ["\r" + item["list_item"] for item in stepsVal]
    
    # grab Categories from DB
    allCategories = mongo.db.categories.find()

    return render_template("edit-recipe.html", recipe=_recipe, categories=allCategories, ingredients=ingreList, recipeSteps=stepsList)


# method to handle the updating of a recipe entry in the Database
@app.route("/update-recipe/<recipe_id>", methods=["POST"])
def updateRecipe(recipe_id):
    recipeDB = mongo.db.recipes

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
        recipeDB.update_one(queryId, {"$unset": {"recipe_allergens": 1}})

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
    recipeDB.update_one(queryId, {"$set": updatedValues})

    # Re-direct to home page
    return redirect(url_for("index"))


######## Delete a Recipe

# remove recipe handler
@app.route("/delete-recipe/<recipe_id>")
def deleteRecipe(recipe_id):
    recipeDB = mongo.db.recipes

    # Delete the Recipe entry in the MongoDB database
    recipeDB.delete_one({"_id": ObjectId(recipe_id)})

    # Re-direct to home page
    return redirect(url_for("index"))


######## Filtering of Recipes

# method to handle filtering of recipes
@app.route("/filter-view", methods=["POST"])
def filterRecipes():
    # grab recipes which match the requested category
    filteredRecipes = mongo.db.recipes.find({"category_name": request.form["filter_category"]})

    # grab number of recipes with category matching the user selected one.
    # this will be used in the front end, if it's a value of '0' then a message will be displayed on front end.
    filteredCount = mongo.db.recipes.find({"category_name": request.form["filter_category"]}).count()

    return render_template("filter-recipes.html", pageTitle="Filtered Recipes - {}".format(request.form["filter_category"]), 
    recipes=filteredRecipes, categorySelected=request.form["filter_category"], recipeCount=filteredCount)


#************ Categories ************#

# method to handle the categories page
@app.route("/view-categories")
def getCategories():
    # grab all Recipe Categories from database
    _categories = mongo.db.categories.find()

    return render_template("categories.html", pageTitle="Manage Recipe Categories", categories=_categories)


######## Add a Category

# method to handle the adding of a category
@app.route("/add-category")
def addCategory():
    return render_template("add-category.html", pageTitle="Add Category")


# method to handle the inserting of a category to the database
@app.route("/insert-category", methods=["POST"])
def insertCategory():
    categories = mongo.db.categories

    # Add new category entry to database
    categories.insert_one(request.form.to_dict())

    # re-direct to 'Manage Recipe Categories' page
    return redirect(url_for("getCategories"))


######## Edit a Category

# method to handle the editing of a category
@app.route("/edit-category/<category_id>")
def editCategory(category_id):
    _category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    return render_template("edit-category.html", pageTitle="Edit Category", category=_category)


# method to handle the updating of a category in database
@app.route("/update-category/<category_id>", methods=["POST"])
def updateCategory(category_id):
    categories = mongo.db["categories"]

    # used to target the entry we want to update
    queryId = {"_id": ObjectId(category_id)}

    # grabbing the new values from the form submission and using them to create a dictionary
    newValues = {
        "category_name": request.form["category_name"]
    }
    
    # Used to update the entry in the MongoDB database
    categories.update_one(queryId, {"$set": newValues})

    # Re-direct to the 'Manage Recipe Categories' page
    return redirect(url_for("getCategories"))


######## Delete a Category

# method to handle the deleting of a category from database
@app.route("/delete-category/<category_id>")
def deleteCategory(category_id):
    # Delete category from Database
    mongo.db.categories.delete_one({"_id": ObjectId(category_id)})

    # Re-direct to 'Manage Recipe Categories' page
    return redirect(url_for("getCategories"))

if __name__ == "__main__":
    # run app in debugging mode
    app.run(debug=True)