from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.recipes
forms = db.forms

for form in forms.find():
  print form['form']