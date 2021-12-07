# Design


## Web Design
The first major design choice we needed to make in fulfilling our project idea was which tools to use to make our website.

One of our first decisions was to create a React app with NodeJS, a tool featured in one of CS50's tutorials.
We set up a git repository so that we could work on collaboratively. We soon discovered that NodeJS was not exactly what we were looking for; we were better prepared tocreate a site with Flask, similar to the Finance site from problem set 9. In fact, we made a skeleton flask project based off of the Finance problem set.

We ended up reimplementing many of the features present in the Finance problem set, such as logging in and logging out to ensure people would not take advantage of the rating feature in the application if implemented in real life. We used some helper functions from the cs50 python library and the login_required helper function from Finance.

The index.html displays a table with values retrieved from our SQL database. We wrote a number of SQL queries incorporated with python logic to format the data in a way it could presented in a table. We made sure to handle a number of edge cases, such as when a menu item does not have any associated ratings.

There is a table of menu items, a table of users (similar to Finance), and a table of ratings.

The schema of our database:

```
sqlite> .schema
CREATE TABLE menu(id INTEGER, food TEXT, class TEXT, ingredients TEXT, allergens TEXT, PRIMARY KEY (id));
CREATE TABLE users (id INTEGER, username TEXT NOT NULL, hash TEXT NOT NULL, PRIMARY KEY(id));
CREATE UNIQUE INDEX username ON users (username);
CREATE TABLE ratings(id INTEGER, food_id INTEGER, rating INTEGER, user_id INTEGER, ts TIMESTAMP, PRIMARY KEY (id), FOREIGN KEY (food_id) REFERENCES menu(id), FOREIGN KEY (user_id) REFERENCES users(id));
```

We created a new page templates for the rating form, and added a feature with a dynamically generated page for each menu item. We defined a function corresponding to the route "food/<food>" to achieve this.


## Web scraping
In our design process, webs craping was the big question mark. On top of the fact that no one in our group had experience working with web scrapers before, it was apparent that the HUDS website had many flaws in it, including messy formatting, glitches in loading the website, and questionable functionality. So, we began by scouring every inch of the HUDS website, learning when the meals refresh, and going over the code line-by-line to figure out how to best extract the content. We created a pseudocode algorithm to work within that framework, and then needed to find a way to implement the scraper. We chose the BeautifulSoup library ultimately for its ability to shrink down web pages to pertinent information. After much trial and error, we were able to regularly scrape information from the website to great success.


## Hosting

We tried using Heroku to at least host a simple app, but ran into error and could not do such. Unfortunately, because we prioritized functionality and web scraping, we were not able to allocate time to deploy the to the web. However, we encourage users to clone this repository and run the app for themselves!
