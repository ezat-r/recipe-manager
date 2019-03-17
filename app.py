from flask import Flask, url_for, redirect, render_template, request
import json
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "recipe-manager"
app.config["MONGO_URI"] = "mongodb://root:adg37tup@ds133496.mlab.com:33496/recipe-manager"

mongo = PyMongo(app)

# method to handle the '/' route or home page
@app.route("/")
def index():
    # fetch all recipes
    _recipes = mongo.db.recipes.find()

    # return the home page template html, and assign it a pagetitle and send accross the 'pageTitle'
    return render_template("recipes.html", pageTitle="Recipes", recipes=_recipes)

# run app in debugging mode
app.run(debug=True)