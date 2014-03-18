from nltk import word_tokenize
from RecipeStructure import Recipe, Step, Action, Ingredient, Utensil, Time
from recipes import parseRecipe

from bs4 import BeautifulSoup as Soup
import urllib2
from pprint import pprint
import re
import json

#allIngredients = ['cream','cheese','ham','chicken','water','butter','onion','chilies','seasoning','breast','filling','flour','paprika','wine','bouillon','juices','oil'];

allCookActions = ['cool','pound','place','add','boil','reduce','cook','simmer','shred','combine','stir','turn','cover','heat','fold','secure','coat','mix','reduce','transfer','stir-fry','pour','bake','grease','preheat','remove','drain','sprinkle','absorb','arrange','stuff','dissolve','brush'];
#allUtensils = ['bag','heat','pot','skillet','bowl','platter','oven'];
allMeasurements = ['pieces','large','medium','low','medium-low','medium-high','slice','small','teaspoon','tablespoon','tsp']
allConditions = ['medium-low','pink','softened','translucent','low','medium','high','clear','minutes','seconds','hours']

class RecipeFlowchart:
	allNodes = [];
	currentNode = None;
	firstNode = None;
	myrecipe = None;
	stringbuffer = "";
	ingredients = [];
	actions = [];
	utensils = [];

	def __str__ (self):
		rv = ""
		for n in self.allNodes:
			rv += str(n);
		return rv;

	def __init__ (self):
		self.allNodes = [];
		self.currentNode = None;
		self.firstNode = None;
		self.myrecipe = None;
		self.stringbuffer = "";
		self.ingredients = [];
		self.actions = [];
		self.utensils = [];

	def setupNodes (self):
		stringbuffer = "";

		self.myrecipe = Recipe();
		self.startNewRecipeStep("");
		self.allNodes = [];

		allIngredients = [];
		for i in self.ingredients:
			allIngredients.append(i.name);

		allUtensils = [];
		for u in self.utensils:
			allUtensils.append(u.name);

		firstNode = Node([""],"first node");
		firstNode.action = "startNewRecipeStep";

		# In Node
		inNode = Node(['in'], "in node");

		# First utensil node
		firstUtensil = Node(allUtensils, "first utensil");
		firstUtensil.action = "addUtensil";
		inNode.addNode(firstUtensil);

		# Cook Node
		cookAction = Node(allCookActions,"cook action");
		cookAction.action = "addAction";
		firstUtensil.addNode(cookAction);

		# Addition Node
		additionWordsAction = Node(['onto','with','together','each'], "addition node");
		cookAction.addNode(additionWordsAction);

		# Measurement Node 1
		measurements1Action = Node(allMeasurements, "0measurement");

		cookAction.addNode(measurements1Action);
		additionWordsAction.addNode(measurements1Action);

		# Ingredient Node 1

		ingredients1Action = Node(allIngredients, "0ingredient");
		ingredients1Action.action = "addIngredient";

		ingredients1Action.addNode(ingredients1Action);
		ingredients1Action.addNode(measurements1Action);

		measurements1Action.addNode(ingredients1Action);
		cookAction.addNode(ingredients1Action);
		additionWordsAction.addNode(ingredients1Action);

		# Utensils Node 1
		uten1Action = Node(allUtensils, "0utensil");
		uten1Action.action = "addUtensil";

		uten1Action.addNode(uten1Action);
		uten1Action.addNode(measurements1Action);

		measurements1Action.addNode(uten1Action);
		cookAction.addNode(uten1Action);
		additionWordsAction.addNode(uten1Action);

		# Addition Node 2
		additionWords2Action = Node(['onto','with','in','on'],"addition node 2");
		ingredients1Action.addNode(additionWords2Action);
		measurements1Action.addNode(additionWords2Action);
		uten1Action.addNode(additionWords2Action);
		cookAction.addNode(additionWords2Action);

		# Measurement Node 2

		measurements2Action = Node(allMeasurements, "1measurement");

		additionWords2Action.addNode(measurements2Action);

		# Ingredient Node 2

		ingredients2Action = Node(allIngredients, "1ingredient");
		ingredients2Action.action = "addIngredient";

		ingredients2Action.addNode(ingredients2Action);
		ingredients2Action.addNode(measurements2Action);

		measurements2Action.addNode(ingredients2Action);
		additionWords2Action.addNode(ingredients2Action);

		# Utensils Node 2
		uten2Action = Node(allUtensils, "1utensil");
		uten2Action.action = "addUtensil";

		uten2Action.addNode(uten2Action);
		uten2Action.addNode(measurements2Action);

		measurements2Action.addNode(uten2Action);
		additionWords2Action.addNode(uten2Action);

		# Until Over Node
		untilOverAction = Node(['until','over'],"until over");

		cookAction.addNode(untilOverAction);
		ingredients1Action.addNode(untilOverAction);
		measurements1Action.addNode(untilOverAction);
		ingredients2Action.addNode(untilOverAction);
		measurements2Action.addNode(untilOverAction);
		uten1Action.addNode(untilOverAction);
		uten2Action.addNode(untilOverAction);

		# Measurement Node 3

		measurements3Action = Node(allMeasurements, "2measurement");

		untilOverAction.addNode(measurements3Action);

		# Ingredient Node 3

		ingredients3Action = Node(allIngredients, "2ingredient");
		ingredients3Action.action = "addIngredient";

		ingredients3Action.addNode(ingredients3Action);
		ingredients3Action.addNode(measurements3Action);

		measurements3Action.addNode(ingredients3Action);
		untilOverAction.addNode(ingredients3Action);

		# Utensils Node 3
		uten3Action = Node(allUtensils, "2utensil");
		uten3Action.action = "addUtensil";

		uten3Action.addNode(uten3Action);
		uten3Action.addNode(measurements3Action);

		measurements3Action.addNode(uten3Action);
		untilOverAction.addNode(uten3Action);

		# Is Are Node
		isAreAction = Node(['is','are'],"is are");

		ingredients3Action.addNode(isAreAction);
		measurements3Action.addNode(isAreAction);
		uten3Action.addNode(isAreAction);

		# To For Node
		toForNode = Node(['to','for'],"to for");

		cookAction.addNode(toForNode);
		ingredients1Action.addNode(toForNode);
		measurements1Action.addNode(toForNode);
		uten1Action.addNode(toForNode);
		uten2Action.addNode(toForNode);
		untilOverAction.addNode(toForNode);

		# Or Node
		orNode = Node(['or'],"or node");

		ingredients2Action.addNode(orNode);
		measurements2Action.addNode(orNode);
		uten2Action.addNode(orNode);

		# Condition Node
		conditionNode = Node(allConditions, "condition node");
		conditionNode.action = "addCondition";

		toForNode.addNode(conditionNode);
		isAreAction.addNode(conditionNode);
		ingredients3Action.addNode(conditionNode);
		uten3Action.addNode(conditionNode);
		measurements3Action.addNode(conditionNode);

		conditionNode.addNode(conditionNode);
		conditionNode.addNode(orNode);
		conditionNode.addNode(untilOverAction);
		conditionNode.addNode(additionWords2Action);

		# And Node
		andNode = Node(['and'],"and node");

		conditionNode.addNode(andNode);

		andNode.addNode(ingredients3Action);
		andNode.addNode(uten3Action);
		andNode.addNode(measurements3Action);
		andNode.addNode(conditionNode);

		# And Node 2
		andNode2 = Node(['and'],"and node 2");

		cookAction.addNode(andNode2);

		andNode2.addNode(cookAction);


		firstNode.addNode(cookAction);
		firstNode.addNode(inNode);
		self.firstNode = firstNode;
		self.currentNode = self.firstNode;

		self.allNodes.append(inNode);
		self.allNodes.append(firstUtensil);
		self.allNodes.append(cookAction);
		self.allNodes.append(additionWordsAction);
		self.allNodes.append(ingredients1Action);
		self.allNodes.append(measurements1Action);
		self.allNodes.append(uten1Action);
		self.allNodes.append(additionWords2Action);
		self.allNodes.append(ingredients2Action);
		self.allNodes.append(measurements2Action);
		self.allNodes.append(uten2Action);
		self.allNodes.append(untilOverAction);
		self.allNodes.append(ingredients3Action);
		self.allNodes.append(measurements3Action);
		self.allNodes.append(uten3Action);
		self.allNodes.append(isAreAction);
		self.allNodes.append(toForNode);
		self.allNodes.append(orNode);
		self.allNodes.append(conditionNode);
		self.allNodes.append(andNode);
		self.allNodes.append(andNode2);

	def step (self, istring):
		#print("\t" + self.currentNode.name + "  " + istring);
		self.stringbuffer = self.stringbuffer + " " + istring;

		# Only advance if the string is accepted as the next node or indicates the start of a new step
		for n in self.currentNode.nextNodes:
			if n.checkNode(istring):
				if "ingredient" in n.name:
					n.doAction(self, istring);
				else:
					n.doAction(self, self.stringbuffer);
				self.currentNode = n;
				if not "measure" in n.name:
					self.stringbuffer = "";
				#print(istring + " " + n.name);
				return;

		for n in self.firstNode.nextNodes:
			if n.checkNode(istring):
				if self.stringbuffer.endswith(istring):
   					self.stringbuffer = self.stringbuffer[:-len(istring)];
				self.firstNode.doAction(self, self.stringbuffer);
				self.stringbuffer = istring;

				#print("\n\nNew Step");
				n.doAction(self, self.stringbuffer);
				self.stringbuffer = "";
				self.currentNode = n;
				return;
		return;

	def startNewRecipeStep (self, iname):
		if self.stringbuffer != "":
			self.addConditionToLastStep(self.stringbuffer);
			self.stringbuffer = "";
		self.myrecipe.addStep(Step("stepName"));

	def addActionToLastStep (self, iname):
		myaction = Action(iname);
		self.myrecipe.getLastStep().addAction(myaction);

	def addIngredientToLastStep (self, iname):
		for i in self.ingredients:
			if iname in i.name:
				self.myrecipe.getLastStep().addIngredient(i);
				return;

	def addUtensilToLastStep (self, iname):
		myuten = Utensil(iname);
		self.myrecipe.getLastStep().addUtensil(myuten);

	def addConditionToLastStep (self, iname):
		mytime = Time(iname);
		self.myrecipe.getLastStep().addTime(mytime);

class Node:
	name = '';
	isTrueNode = False;
	values = '';
	nextNodes = [];
	action = "";

	def __init__ (self, ival, iname):
		self.name = iname;
		self.nextNodes = [];
		self.values = [];
		if isinstance(ival, basestring):
			self.values = [ival];
		else:
			for i in ival:
				self.values.append(i);

	def __str__ (self):
		rv = self.name + ": \n";
		for n in self.nextNodes:
			rv += "\t" + n.name + "\n";
		return rv;

	def checkNode(self, ival):
		for v in self.values:
			if v == ival:
				return True;
		return False;

	def addNode (self, node):
		self.nextNodes.append(node);

	def doAction (self, recipe, parameter):
		if not self.action == None:
			if self.action == "startNewRecipeStep":
				recipe.startNewRecipeStep(parameter);
			if self.action == "addAction":
				recipe.addActionToLastStep(parameter);
			if self.action == "addIngredient":
				recipe.addIngredientToLastStep(parameter);
			if self.action == "addUtensil":
				recipe.addUtensilToLastStep(parameter);
			if self.action == "addCondition":
				recipe.addConditionToLastStep(parameter);

def parseUtensils(istring):
	# Loop through our list of utensils and compare every word with the list returning everything that matches.
	istring = word_tokenize(istring);

	f = open('utensils.csv', 'r')
	utensilList = f.read().split('\r');

	rv = [];

	for s in istring:
		for u in utensilList:
			if u.split(',')[0].lower() in s.lower():
				newU = Utensil(u.split(',')[0].lower());
				rv.append(newU);
				print(u.split(',')[0].lower());

	return rv;

def expandMeasure(istring):

	if not istring:
		return "none";

	allMeasures = ["fluid ounce", "teaspoon","tablespoon","ounce","pound","gallon","inch","pint","quart","dozen"];

	if "istring" in allMeasures:
		return istring;
	else:
		if "fl" in istring and "oz" in istring:
			return "fluid ounce";
		if "tsp" in istring:
			return "teaspoon";
		if "tbsp" in istring or "tbs" in istring:
			return "tablespoon";
		if "oz" in istring:
			return "ounce";
		if "lb" in istring:
			return "pound";
		if "gal" in istring:
			return "gallon";
		if "in" in istring:
			return "inch";
		if "pt" in istring:
			return "pint";
		if "qt" in istring:
			return "quart";
		if "doz" in istring:
			return "dozen"
		return istring;

def parseStringRecipe (istring):
	#istring = "Heat the butter in a skillet over medium heat. Stir in the onion; cook and stir until the onion has softened and turned translucent, about 5 minutes. Add the shredded chicken, chopped green chilies, taco seasoning, half of the bunch of chopped green onion, and water."
	#istring = "Pound chicken breasts if they are too thick. Place a cheese and ham slice on each breast within 1/2 inch of the edges. Fold the edges of the chicken over the filling, and secure with toothpicks. Mix the flour and paprika in a small bowl, and coat the chicken pieces. Heat the butter in a large skillet over medium-high heat, and cook the chicken until browned on all sides. Add the wine and bouillon. Reduce heat to low, cover, and simmer for 30 minutes, until chicken is no longer pink and juices run clear. Remove the toothpicks, and transfer the breasts to a warm platter. Blend the cornstarch with the cream in a small bowl, and whisk slowly into the skillet. Cook, stirring until thickened, and pour over the chicken. Serve warm."
	#istring = "In a small bowl, combine the soy sauce, rice wine, brown sugar and cornstarch. Set aside. Heat oil in a wok or skillet over medium high heat. Stir-fry ginger and garlic for 30 seconds. Add the steak and stir-fry for 2 minutes or until evenly browned. Add the snow peas and stir-fry for an additional 3 minutes. Add the soy sauce mixture, bring to a boil, stirring constantly. Lower heat and simmer until the sauce is thick and smooth. Serve immediately.";

	html = urllib2.urlopen(istring).read();

	soup = Soup(html)

	recipeText = soup.find(itemprop='recipeInstructions').get_text();
	print(recipeText);


	recipe = parseRecipe(istring);

	ingredients = [];
	for i in recipe:
		ingredName = i['ingredient'];
		if ',' in ingredName:
			ingredName = word_tokenize(ingredName.split(',')[0]);
			ingredName = ingredName[len(ingredName) - 1];
		ingredName = word_tokenize(ingredName)[len(word_tokenize(ingredName)) - 1];

		ingred = Ingredient(ingredName);
		ingred.form.append(i['form']);
		if i['quantity']:
			ingred.quantity = i['quantity'];
		else:
			ingred.quantity = 1;
		ingred.unit = i['measurement'];
		ingredients.append(ingred);


	recipeText = recipeText.lower();
	recipeText = re.sub('[.]','',recipeText);
	myrfc = RecipeFlowchart();

	for i in ingredients:
		myrfc.ingredients.append(i);

	utensils = parseUtensils(recipeText);

	for u in utensils:
		myrfc.utensils.append(u);

	myrfc.setupNodes();

	recipeText = word_tokenize(recipeText);

	for i in recipeText:
		myrfc.step(i);

	print(myrfc.myrecipe);
	utensilNames = []
	for u in utensils:
		utensilNames.append(u.name);
	utensilNames= list(set(utensilNames));

	prettyIngredients = []
	for i in ingredients:
		prettyIngredients.append({"name":i.name, "quantity":float(str(i.quantity)), "measurement":expandMeasure(i.unit), "descriptor":str(i.form[0]).lower(), "preparation":i.descriptor})

	rv = json.dumps({"ingredients":prettyIngredients, "cooking tools":utensilNames, "cooking method":"bake"});
	rv = rv.lower();
	print(rv);

	#print(myrfc);

#istring = "Place the chicken in a large pot and add water to cover. Bring to a boil over high heat, then reduce the heat to medium-low, cover, and simmer until the chicken pieces are no longer pink, about 10 minutes.";

recipeURL = raw_input("Enter a recipe URL: ")

istring = 'http://allrecipes.com/Recipe/Moroccan-Style-Stuffed-Acorn-Squash/Detail.aspx?prop24=RD_RelatedRecipes';
parseStringRecipe(recipeURL);