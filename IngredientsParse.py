# part of number 2 on the assignment sheet

from bs4 import BeautifulSoup as Soup
import urllib, re, string
from pprint import pprint

preparations = [line.strip() for line in open('preparations.txt')]
descriptors = [line.strip() for line in open('descriptors.txt')]

def parseIngredient(html):

  name, quantity, measurement, preparation, descriptor = (None, None, None, None, None)

  amount_span = html.find('span', class_='ingredient-amount')
  amount = amount_span.string if amount_span else None
  if amount:
    match = re.search('(\d.*\d*)\s(\w+)', amount)
    quantity = match.group(1) if match else amount
    measurement = match.group(2) if match else None

  ingredient_span = html.find('span', class_='ingredient-name')
  ingredient = ingredient_span.string if ingredient_span else None

  name = ingredient

  for p in preparations:
    if p in name:
      preparation = p
      name = name.replace(p, '')
      break

  for d in descriptors:
    if d in name:
      descriptor = d
      name = name.replace(d, '')
      break

  name = "".join(l for l in name if l not in string.punctuation).strip()

  parsed_ingredient = {
    "quantity": quantity,
    "measurement": measurement,
    "preparation": preparation,
    "descriptor": descriptor,
    "name": name
  }

  return parsed_ingredient

recipeURL = raw_input("Enter a recipe URL: ")
html = Soup(urllib.urlopen(recipeURL))

ingredients = html.find_all(id="liIngredient")

output = {'ingredients': map(parseIngredient, ingredients)}

pprint(output)
