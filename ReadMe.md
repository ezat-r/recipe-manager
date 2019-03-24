# Recipe Management System

A recipe managment system allowing users to create, read, update and delete recipes.

## Demo

To view the project in action, visit the following link:

https://recipe-flask-manager.herokuapp.com/

## UX

The Recipe Management System uses the CRUD principles and allows users to create, read, update and delete recipes on a web based platform.

### Mockups

Initial mockups were made using **Balsamiq** software to aid in the creation of the website; a basic mockup was made of each web page. 
- The mockups can be found in the **Mockups** folder. 

## Features

- **Creation of Recipes** - The project provides a user friendly web ui for users to create recipes.
    - Icons and Placeholder text, as well as, JQuery triggered text helper messages are applied across all input fields on the *Add New Recipe* page, to make it easier and intuitive for users to add recipes without fault.

- **Viewing of Recipes** - the project home page shows a list of recipes already created, in a visual pleasing way.
    - All properties of a recipe can be viewed by all users using the website.
    - *Views* -> the view  property is added to each recipe and is used to keep track of how many times a particular recipe has been viewed by other users.

- **Updating of Recipes** - the project allows users to go in and update or add on to their favourite recipes, with ease. 

- **Deleting of Recipes** - the project also allows users to delete recipes, all at the touch of a button. 

- **Filtering of Recipes** - the project allows users to filter their favourite recipes. The filter uses the Recipe Category property to filter recipes and allows users to filter their favourite recipes.

## Technologies Used

List of tools and technologies used in this project are as follows:

- [Materialize CSS](https://materializecss.com/)
    - The project uses **Materialize CSS** to simplify the web page design and to maintain consistency across multiple browsers and screen resolutions. Materialize icons were also used throughout the project such as button icons etc.
- [JQuery](https://jquery.com)
    - The project uses **JQuery** to aid with the Materialize CSS navigation and various other components across the project use it to function correctly. I also used JQuery to write my own custom code for the handling of the Pagination.
- [Python](https://www.python.org/)
    - The **Python** programming language was used to code the backend of the Recipe Management project.
- [Flask](http://flask.pocoo.org/)
    - The project uses **Flask** which is a Python framework used as the backend of the project and fulfilling functions such as; connecting to the MongoDB database, controlling routing and navigation across pages etc.
- [MongoDB](https://mlab.com/)
    - The project uses **MongoDB** as the Database to store recipes; in particular MLab hosting service is used.
- [Heroku](https://www.heroku.com/)
    - The project uses **Heroku** as the Hosting platform for this project; this was because GitHubPages only provides hosting for static projects, and not dynamic projects like this Recipe Manager project.
- [Font Awesome](https://fontawesome.com/)
    - The project uses **Font Awesome** to provide icons for the Footer social network links. 
- [Balsamiq](https://fonts.google.com/specimen/Roboto)
    - This tool was used to create the mockups of the website at the beginning of the project. 


## Database Schema

### Choice of Database

I decided to use **MongoDB** (NoSQL) as the database for this project. The reason is as follows:
- Flexibility; each recipe will be different in some sense, for example; one recipe will contain allergens, whilst another recipe won't etc. mongoDB allows flexibility for this.

### Recipe Properties

After scouring the web and looking at existing Recipe websites, I came up with the following properties which will make up the database:

- *category_name*
- *recipe_title*
- *recipe_author*
- *recipe_description*
- *recipe_duration*
- *recipe_ingredients*
- *recipe_steps*
- *containsAllergens*
- *recipe_allergens*
- *recipe_views*

### Relationship between Recipes & Properties

The following properties will have a 1-2-1 relationship with a recipe:

- *category_name* - this is a property which determines the origin of the cuisine. Examples include: British, Japanese, Thai etc.
- *recipe_title* - this is the recipe title or name.
- *recipe_author* - this is the recipe's author.
- *recipe_description* - this is the recipe's author.
- *recipe_duration* - this is the recipe duration.
- *containsAllergens* - this is true or false variable which determines if there are allergens present in a recipe.
- *recipe_allergens* - this is the recipe allergens.

Properties which have a 1-2-many relationship will make use of nesting to organise them in the **MongoDB** database. The following properties will have a 1-2-many relationship with a recipe:

- *recipe_ingredients* - this is a list of recipe ingredients.
- *recipe_steps* - this is a list of recipe steps.

## Testing

Majority of the Testing for this project was Web UI testing i.e. go to a page and make sure it looks fine, click a button and make sure it does what it's supposed to do etc.

### Web UI Testing
Testing scenarios run:

1. Navigation:
    1. Click on all main navigation buttons i.e. 'Home', 'Add New Recipe' and 'Manage Categories'. Verify that each button takes you to the correct page.
    2. Click onto the 'Recipe Manager' brand name in the top-left of each page and verify that it takes you to the 'Recipes' page.

2. Forms testing:
    1. Go to the "Add New Recipe" page.
    2. Try to submit the empty form and verify that an error message about the required fields appears.
    3. Try to submit the form without selecting a 'Recipe Category' and verify that you cannot submit the form.
    4. Try to submit the form with all valid inputs and verify that the recipe is created successfully and you are re-directed to the 'Recipes - Home' page. Verify that the new recipe shows up correctly.
    5. Repeat steps 1-4 for the 'Edit Recipe' and other forms and make sure everything is working as expected.

3. Add Recipe:
    1. Go to the "Add New Recipe" page.
    2. Fill out the form.
    3. Click the *ADD RECIPE* button.
    4. Verify that you are re-directed to the "Recipe Manager - Home" page and the new Recipe can be viewed.

4. Edit Recipe:
    1. Go to the "Recipe Manager - Home" page.
    2. Click the *EDIT* button for one of your Recipes.
    3. Make some changes and then click the *UPDATE RECIPE* button.
    4. Verify that you are re-directed to the "Recipe Manager - Home" page and the updates are applied to the Recipe.

5. Delete Recipe:
    1. Go to the "Recipe Manager - Home" page.
    2. Click the *View* button for one of the recipes on display.
    3. Click the *DELETE* button at the bottom of the page.
    4. Verify that you are re-directed to the "Recipe Manager - Home" page and the deleted Recipe is no longer visible on the page.

5. Detailed Recipe View:
    1. Go to the "Recipe Manager - Home" page.
    2. Click the *View* button for one of the recipes on display.
    3. Verify that all the information on the page is correct.

6. Typography:
	1. Go to the "Recipe Manager - Home" page.
	2. Have a look at the text and observe if all text is clearly visible i.e. is it too small, too big.
    3. Click the 'View' button to access a detailed Recipe view and verify that the text looks readable, is not hard to read etc.
	4. Follow step 2-3 again, however, this time do the same for different screen sizes i.e. Phone, Tablet, Desktop etc.
	5. Follow steps 2 - 4 for all pages. Is the the typography consistent across all pages? Is it readable on small screen devices?

### Python Code Tests

Instead of using a framework to test my code, like I did in Section 5, I used Python in order to Test certain aspects of my Python code.
- I made use of *assertions* to make sure that the actual results of the tests matched the expected outputs

In the app.py there are 2 functions which I've written tests for; the *checkAllergens* function & the *listifyDict* function. The tests are in the *tests.py* file which can be found in the **Tests** folder.

#### 'checkAllergens' Function - Why it's needed and how it was tested:

As part of the Add & Edit Recipe forms, I've used a toggle switch button which the user can set to 'On' or 'Off'. When the 'Contains Allergens' switch is set to the 'On' state, it then brings into view the 'Allergens' input field which allows a user to enter allergen related information.

However, there was an issue with the submission of forms which had the 'Contains Allergens' switch disabled; when it was set to 'Off' the switch elements value was not submitted as part of the form;
- this led to issues in the backend because the code in the backend depended on the 'containsAllergens' value in the form submission data, but because it wasn't included, it threw errors. So to get around this issue, I created the *checkAllergens* function. The function takes the formData dict as a parameter and checks for the presence of a 'containsAllergens' dict key; if one is present then a value of *True* is returned, otherwise if there is no entry whatsoever, then a value of *False* is returned. This resolved the issue in the backend when carrying out actions such as Adding a new recipe or Updating an existing one in the MongoDB database.

The *checkAllergens* function was tested by passing various dummy inputs and using Python **assertions** to check the output.

#### 'listifyDict' Function - Why it's needed and how it was tested:

As part of the Add & Edit Recipe forms, the 'Recipe Ingredients' and 'Recipe Steps' properties had a *textarea* tag as the HTML Form Element.

However, when users entered multiple lines of text into the textarea's and submitted the form, in the backend a value was returned which contained various carriage returns and new line escape characters (\r\n) separating each line of text, which when viewed in the web ui was not very nice and gave bad user experience.
- To solve this, the *listify* function was created. The function takes a string value as a parameter and checks for the presence of '\r\n' characters; if present then the value is split and stored into a list variable. Then, the list is used to create another list of key-value dicts with each one holding a line of text entry of the parameter. This list of key-value pairs is then returned. 
    - If there are no '\r\n' characters present in the parameter, then a list consisting of a single dict is returned; the dict has the value equal to the parameter being passed to the function.
- This function made it easier to display *recipe_ingredients* and *recipe_steps* on the web ui.

The *listifyDict* function was tested by passing various dummy inputs and using Python **assertions** to check the output.

### Screen Size & Different Browsers

#### Screen Sizes

Using the Debugger tools on Google Chrome I was able to view the website in different screen sizes. The following screen sizes were verified:
- 360px X 640px (WxH)
- 768px X 1024px (WxH)
- 1024px X 1366px (WxH)

Test's were run for various screen sizes, these are listed in the above **Testing** section.

On smaller screen sizes i.e. when the width is 768px or less, the website switches to a stacked view to maintain a consistent look.

#### Multi Browser Testing

Multi browser testing was carried out to ensure there is consistency across different Browsers. The following Browsers were tested:
- Google Chrome
- Mozilla Firefox
- Microsoft Edge
- Internet Explorer v11

## Deployment

The website was deployed using Heroku. Deployment process which was followed is given below:

1. Login to Heroku dashboard.
2. Create a new *App* - for location select *Europe*.
3. Once the app has been created, click the **Settings** tab and copy the *Heroku GIT URL*.
4. Go into your app settings and click the *Reveal Config Vars* button and add an entry for your **IP** & **PORT**.
5. Go into your Cloud9 and enter the following command in the terminal: git remote add heroku https://heroku-git-url.git -> replace the url with your appropriate one.
6. Run the following command to create a *requirements.txt* file: **pip3 freeze --local > requirements.txt**
7. Create a *Procfile* by running the following command: **echo web: python app.py > Procfile**
8. Do a git commit to push all changes to your local repository and run the following command: **git push -u heroku master**
9. Access your heroku app link to see deployment.
10. Your app is now deployed onto Heroku.
