#
# RecipeStructure.py
# All recipes and their components are stored in this format
#

import json


# The highest data type, a recipe. It contains a linked list of steps
class Recipe:
	firstStep = None;			# The first step in our recipe. A Step object pointing to the next step
	allIngredients = [];		# A set of all the ingredients our recipe uses
	allUtensils = [];			# Same for utensils
	allActions = [];			# and actions

	def __init__(self):		# Constructor
		self.firstStep = None;

	def __str__ (self):
		rv = "";
		rv += "Ingredients: \n";
		for i in self.allIngredients:
			rv += "\t" + str(i) + "\n";
		rv += "Utensils:\n";
		us = [];
		for u in self.allUtensils:
			us.append(str(u));
		us = list(set(us));
		for u in us:
			rv += "\t" + str(u) + "\n";
		currentStep = self.firstStep;
		while currentStep != None:
			rv += str(currentStep);
			currentStep = currentStep.nextStep;
		#rv += self.getJSON();
		return rv;

	# Convert the recipe to json, ignoring steps. Only uses the lists of all ingredients, utensils, and actions
	def getJSON (self):
		utensilNames = []

		for u in self.allUtensils:
			utensilNames.append(u.name);
		utensilNames= list(set(utensilNames));

		prettyIngredients = []
		for i in self.allIngredients:
			prettyIngredients.append({"name":i.name, "quantity":float(str(i.quantity)), "measurement":self.expandMeasure(i.unit), "descriptor":str(i.form[0]).lower(), "preparation":i.descriptor})

		rv = json.dumps({"ingredients":prettyIngredients, "cooking tools":utensilNames, "cooking method":self.allActions});
		rv = rv.lower();

		return rv;

	# Add a new step to the recipe
	def addStep(self, inputStep):			# Build the recipes by adding steps to the end
		if self.firstStep == None:
			self.firstStep = inputStep;
		else:
			lastStep = self.firstStep;
			while lastStep.nextStep != None:
				lastStep = lastStep.nextStep;
			inputStep.StepNumber = lastStep.StepNumber + 1;
			lastStep.nextStep = inputStep;

	# Traverse the linked list and get the final step
	def getLastStep (self):
		lastStep = self.firstStep;
		while not lastStep.nextStep == None:
			lastStep = lastStep.nextStep;
		return lastStep;

	# Given a measurement that has been abbreviated, ie tsp, expand it to ie tablespoon
	def expandMeasure(self,istring):

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

# Recipes are made up of steps. Steps have actions, ingredients, and utensils.
class Step:
	name = "";
	previousStep = None;		# The step immediately preceding
	nextStep = None;			# The step immediately after
	StepNumber = 0;				# Which step are we on
	ingredients = [];			# List of all ingredients used in this step
	actions = [];				# List of every action in this step
	times = []; 				# Time object representing the length of the step
	unassigneduten = None;

	def __init__ (self, iname):
		self.name = iname;
		self.previousStep = None;
		self.nextStep = None;
		self.StepNumber = 0;
		self.ingredients = [];
		self.actions = [];
		self.time = [];
		self.unassigneduten = None;

	def __str__ (self):
		rv = "\nStep " + str(self.StepNumber) + "\n";
		if len(self.ingredients) > 0:
			rv += "\tIngredients: \n";
		for i in self.ingredients:
			rv += "\t\t" + str(i) + "\n";
		if len(self.actions) > 0:
			rv += "\tActions: \n"
		for a in self.actions:
			rv += "\t\t" + str(a) + "\n";
		if not self.unassigneduten == None:
			rv += "\tUtensil: \n"
			rv += "\t\t" + str(self.unassigneduten) + "\n";
		if len(self.time) > 0:
			rv += "\tTime: \n";
		for t in self.time:
			rv += "\t\t" + str(t) + "\n";
		return rv + "\n";

	def addIngredient(self, inputIngredient):		# Add an ingredient
		self.ingredients.append(inputIngredient);

	def addAction(self, inputAction):				# Add an action
		if not self.unassigneduten == None:
			if inputAction.utensil == None:
				inputAction.utensil = self.unassigneduten;
				self.unassigneduten = None;
		self.actions.append(inputAction);

	def addTime(self,time):						# How long the step takes
		self.time.append(time);

	def addUtensil(self,uten):
		if len(self.actions) > 0:
			for a in self.actions:
				if a.utensil == None:
					a.utensil = uten;
					return;
			self.unassigneduten = uten;
		else:
			self.unassigneduten = uten;

	def changeStyle(self,tag):					# Change all ingredients in the step to some style
		for ingred in ingredients:
			if not ingred.isTag(tag):
				ingred.getTagSubstitute(tag);

class Ingredient:
	name = "";						# What's it called
	quantity = 0;					# How much is required
	unit = None;					# What units
	tags = []; 						# All tags that describe the ingredient ie, Dairy, vegetarian, poultry
	substitutes = []; 				# All ingredients that could substitute for this one
	form = [];						# What form is the ingredient ie chopped, diced
	descriptor = "none";			# Something that describes the ingredient

	def __init__ (self, iname):
		self.name = iname;
		self.unit = "unit";

	def __str__ (self):
		return self.name + " (" + str(self.form[0]) + ", " + self.descriptor + ")" + ": " + str(self.quantity) + " " + str(self.unit);

	def isTag(tag):					# Does the ingredient have some tag
		if tag in tags:
			return true;
		else:
			return false;

	def getTagSubstitute(tag):			# Find a substitute ingredient that conforms to this tag
		if self.isTag(tag):
			return self;
		else:
			for s in substitutes:
				if s.isTag(tag):
					return s;


class Action:
	name = "";				# What is being done here
	utensil = None;			# What are we using to do it

	def __init__ (self, iname):
		self.name = iname;

	def __str__ (self):
		if self.utensil == None:
			return self.name;
		else:
			return self.name + " Utensil: " + str(self.utensil);

class Unit:
	name = ""; 				# Ie cups, gallons, kilograms

class Form:
	name = ""; 				# From list

class Utensil:
	name = ""; 				# From list

	def __init__ (self, iname):
		self.name = iname;

	def __str__ (self):
		if self.name == 'heat':
			return 'stove';
		else:
			return self.name;

class Time:						# TODO
	name = "";

	def __init__ (self, iname):
		self.name = iname;

	def __str__ (self):
		return self.name;