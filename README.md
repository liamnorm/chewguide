# The Chew Guide
[Video Presentation of Application](https://youtu.be/NyPgp9OGxk8)

## Application Purpose
The purpose of this application is to let people rank the food that Annenberg is serving, in turn letting other people know what the best food at Annenberg is. Since the menu items changes every day, and the food is prepared differently each day.
This is is a Flask application, designed to be hosted on the internet to allow people to log on and rank Annenberg's food.

# Hosting your own local Chew Guide
Here is how to host your own copy of the Chew Guide. You can either clone this git repository or, if you have a retrieved a zipped file from Gradescope, you can use that to run the submitted version.

## Cloning the Chew Guide from GitHub

First, clone this repository.

`$ git clone https://github.com/liamnorm/chewguide.git`

Then continue to "Running the Chew Guide."

## Downloading the Chew Guide from a Zipped File

After you have downloaded the zipped file with all the components (i.e. from Gradescope), extract all and continue to "Running the Chew Guide."

## Running the Chew Guide

Change directory into the chewguide repository.

`$ cd chewguide`

Run the following, if needed, to install the necessary libraries. You will need [pip](https://pip.pypa.io/en/stable/installation/).

`$ pip install sqlite3 cs50 werkzeug flask flask_session requests pandas bs4`

To serve the app on your device, run the following:

`$ flask run`

If you get the error "The term flask is not recognized...", you may need to run

`$ python -m flask run` instead.

Then visit https://127.0.0.1:5000/ in a browser. A login page should appear.

Type Ctrl + C to quit running the Flask app.

## Getting Started

After running the app, you should be faced with the login page in the browser. Register for a Chew Guide on your local server by entering a username and password. After registering you will need to log in again.

## Key Features on the Chew Guide

###### Menu Information

Upon logging in you should see a list of the food Annenberg is serving for a given meal.

###### Specific Food Information

You can click on each food, and it will take you to a page containing its ingredients and allergen information. This allows users to not have to use both the Chew Guide and the HUDS website when trying to get the full picture of what Anneberg is offering on that day.

###### Food Ranking Feature

To rank a menu item, click on Rate in the top corner. This will take you to a page with a rating form.

Select the menu item you want to rate from the drop down list and enter a rating from 1 to 5. Your ranking will be added to the database.

To see how rankings average over multiple users, you can log out, register another account, and rank foods through that account.


To update the menu, run
`python3 web-scraper.py`
`sqlite3 menu.db`
`.mode csv`
`.import menu_items.csv menu`
