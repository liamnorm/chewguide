# web-scraper.py
#
# Identify the foods during the day.
# Export them into a CSV file for further usage.

import requests
import pandas as pd
from bs4 import BeautifulSoup

# Locate the URL of the HUDS website.
URL = "http://www.foodpro.huds.harvard.edu/foodpro/menu_items.asp?type=30&meal=1"

# Retrieve the page using GET.
page = requests.get(URL)

# Testing Purposes: Print out the page's text.
# print(page.text)

# Set up a new HTML parser on the page's content.
soup = BeautifulSoup(page.content, "html.parser")

# Find the content that matches an ID of content.
results = soup.find(id = "content")

# Testing Purposes: Print out the content that matches the find above.
# print(results.prettify())

# Find all the links in the inside of #content.
food_items = results.find_all("a")

# With each link in #content, decide whether it's a valid food or not.
valid_food = False

menu = []
ingredients = []
allergens = []

# Iterate through each a element from the result
for food_item in food_items:

    # Testing Purposes
    # print(food_item, end="\n"*2)

    # All elements past "Create Nutrition Report" will not be food items.
    if food_item.text.strip() == "Create Nutrition Report":
        valid_food = False

    # If the element is a valid food item, add the insides as a text element.
    if valid_food == True:
        # Testing Purposes
        print(food_item.text.strip())

        # Add each element to the menu.
        menu.append(food_item.text.strip())

        # Get the URL for each food item.
        food_url = food_item['href']

        # Retrieve the page using GET.
        food_page = requests.get(food_url)

        # Set up a new HTML parser on the page's content.
        food_soup = BeautifulSoup(food_page.content, "html.parser")

        # Find the content that matches an ID of content.
        results = food_soup.find(id = "content")

        # Find all the paragraphs in the inside of #content.
        food_ps = results.find_all("p")

        # Iterate for ingredients.
        ing_found = False

        for food_p in food_ps:

            # Search for the ingredients within the text.
            if "Ingredients" in food_p.text.strip() and "Consumer Responsibility" not in food_p.text.strip():
                # Add the ingredients to the list.
                ingredients.append(food_p.text.strip())

                # Testing Purposes:
                # print(food_p.text.strip())

                ing_found = True

                break

        if ing_found == False:
            ingredients.append("Ingredients: N/A")
        
        # Iterate for allergens.
        all_found = False

        for food_py in food_ps:

            found = False

            # Search for the allergens within the text.
            if "Allergens" in food_py.text.strip():
                # Add the allergens to the list.
                allergens.append(food_py.text.strip())
                
                # Testing Purposes:
                # print(food_py.text.strip())

                all_found = True

                break

        if all_found == False:
            allergens.append("Allergens: N/A")

    # Elements past "Cancel" are valid food items.
    if food_item.text.strip() == "Cancel":
        valid_food = True

# Testing Purposes
# print("Menu: " + str(len(menu)))
# print("Ingredients: " + str(len(ingredients)))
# print("Allergens: " + str(len(allergens)))

# Convert the lists to a dictionary.
dict = {"item": menu, "ingredients": ingredients, "allergens": allergens}

# Send the dictionary to a Pandas Dataframe.
df = pd.DataFrame(dict)

# Convert the file to a CSV for processing into SQL.
df.to_csv("menu_items.csv")