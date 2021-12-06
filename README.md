# The Chew Guide

This is is a Flask application.

# How to Use

Here is how to host your own copy of the Chew Guide.

First, clone this repository.

`$ git clone https://github.com/liamnorm/chewguide.git`

Change directory into the chewguide repository.

`$ cd chewguide`

Run the following, if needed, to install the necessary libraries. You will need [pip](https://pip.pypa.io/en/stable/installation/).

`$ pip install cs50`

`$ pip install werkzeug`

`$ pip install flask`

`$ pip install flask_session`

To serve the app on your device, run the following:

`$ flask run`

Then visit https://127.0.0.1:5000/ in a browser.

You should be faced with the login page. Register for a Chew Guide on your local server by entering a username and password. After registering you will need to log in again.

Upon logging in you should see a list of the food Annenberg is serving for the day.

To rank a menu item, click on Rate in the top corner. This will take you to a page with a rating form.

Select the menu item you want to rate from the drop down list and enter a rating from 1 to 5. Your ranking will be added to the database.

To see how rankings average over multiple users, you can log out, register another account, and rank foods through that account.
