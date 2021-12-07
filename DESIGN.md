# Design


## Web Design
The first major design choice we needed to make in fulfilling our project idea was which tools to use to make our website.

One of our first decisions was to create a React app with NodeJS, a tool featured in one of CS50's tutorials.
We set up a git repository

We  decided it would be easiest to create a site with Flask, similar to the Finance site problem set 9.
In fact, we made a skeleton flask project based off of the Finance problem set.

We ended up reimplementing many of the features present in the Finance problem set, such as logging in and logging out to ensure people would not take advantage of the rating feature in the applcation if implemented in real life. We used some helper functions from the cs50 python library and the login_required helper function from Finance.

The index.html displays a table with 

## Webscraping
In our design process, webscraping was the big question mark. On top of the fact that no one in our group had experience working with web scrapers before, it was apparent that the HUDS website had many flaws in it, including messy formatting, glitches in loading the website, and questionable functionality. So, we began by scouring every inch of the HUDS website, learning when the meals refresh, and going over the code line-by-line to figure out how to best extract the content. We created a pseudocode algorithm to work within that framework, and then needed to find a way to implement the scraper. We chose the BeautifulSoup library ultimately for its ability to shrink down web pages to pertinent information. After much trial and error, we were able to regularly scrape information from the website to great success.

###### Basic Menu Items

###### Ingredients and Allergen Information

###### Meal-Based Updates 


## Hosting
