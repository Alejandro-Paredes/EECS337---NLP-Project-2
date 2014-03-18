from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.recipes
recipes = db.recipes
forms = db.forms

for recipe in recipes.find():
  for ingredient in recipe['ingredients']:
    name = ingredient['ingredient_name']
    if name:
      if ', ' in name:
        form = name.split(', ', 1)[1]
        forms.update({'form':form}, {'name': name, 'form':form}, True)
      if ' - ' in name:
        form = name.split(' - ', 1)[1]
        forms.update({'form':form}, {'name': name, 'form':form}, True)