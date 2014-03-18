from bs4 import BeautifulSoup as Soup
import urllib
from pprint import pprint
import re

forms = [line.strip() for line in open('forms.txt')]

def parseIngredient(html):

  quantity = None
  measurement = None
  form = None
  ingredient = None

  amount_span = html.find('span', class_='ingredient-amount')
  amount = amount_span.string if amount_span else None
  if amount:
    match = re.search('(\d\s?\d*)\s(\w+)', amount)
    quantity = match.group(1) if match else None
    measurement = match.group(2) if match else None

  ingredient_span = html.find('span', class_='ingredient-name')
  ingredient = ingredient_span.string if ingredient_span else None

  if ingredient:
    for f in forms:
      if f in ingredient:
        regex = "(%s)\s(.+)" % f
        form = f
        if re.search(regex, ingredient): ingredient = re.search(regex, ingredient).group(2)

  parsed_ingredient = {
    "quantity": quantity,
    "measurement": measurement,
    "form": form,
    "ingredient": ingredient
  }

  print parsed_ingredient
  return parsed_ingredient

def parseRecipe(url):
  html = Soup(urllib.urlopen(url))
  ingredients = html.find_all(id="liIngredient")
  print "=============================="
  return map(parseIngredient, ingredients)


#html = Soup(urllib.urlopen('http://allrecipes.com/recipes/everyday-cooking/vegetarian/?prop24=hn_slide0&evt19=1'))
#recipe_links = ['http://allrecipes.com' + recipe.find('a', class_='title')['href'] for recipe in html.find_all(class_='recipe-info')]

#recipes = map(parseRecipe, recipe_links)

#pprint(recipes)