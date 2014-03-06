class Recipe:
	firstStep = None;			# The first step in our recipe. A Step object

	def __init__(self, step):		# Constructor
		self.firstStep = step;

	def __str__ (self):
		rv = "";
		currentStep = firstStep:
		while currentStep != None:
			rv += str(currentStep);
			currentStep = currentStep.nextStep;
		return rv;

	def addStep(inputStep):			# Build the recipes by adding steps to the end
		lastStep = firstStep;
		while lastStep != None:
			lastStep = firstStep.nextStep;
		inputStep.StepNumber = lastStep.StepNumber + 1;
		lastStep.nextStep = inputStep;

	def deleteLastStep():			# Delete the final step
		Step lastStep = firstStep;
		while lastStep != None:
			lastStep = firstStep.nextStep;
		lastStep.previousStep.nextStep = None;

class Step:
	previousStep = None;		# The step immediately preceding
	nextStep = None;			# The step immediately after
	StepNumber = 0;				# Which step are we on
	ingredients = [];			# List of all ingredients used in this step
	actions = [];				# List of every action in this step
	time = None; 				# Time object representing the length of the step

	def __str__ (self):
		rv = "Step " + StepNumber + "\n";
		rv += "Combine: \n";
		for i in ingredients:
			rv += "\t" + str(i) + "\n";
		rv += "And then: \n"
		for a in actions:
			rv += "\t" + str(a) + "\n";
		rv += "For " + str(time);
		return rv;

	def AddIngredient(inputIngredient):		# Add an ingredient
		ingredients.append(inputIngredient);

	def AddAction(inputAction):				# Add an action
		actions.append(inputAction);

	def SetTime(time):						# How long the step takes
		self.time = time;

	def changeStyle(tag):					# Change all ingredients in the step to some style
		for ingred in ingredients:
			if !ingred.isTag(tag):
				ingred.getTagSubstitute(tag);

class Ingredient:
	name = "";						# What's it called
	quantity = 0;					# How much is required
	unit = None;					# What units
	tags = []; 						# All tags that describe the ingredient ie, Dairy, vegetarian
	substitutes = []; 				# All ingredients that could substitute for this one
	form = "";						# What form is the ingredient ie chopped, diced

	def __init__ (self, iname):
		self.name = iname;

	def __str__ (self):
		return self.name;

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
		return self.name + " with a " + str(utensil);

class Unit:
	name = ""; 				# Ie cups, gallons, kilograms

class Form:
	name = ""; 				# From list

class Utensil:
	name = ""; 				# From list

	def __str__ (self):
		return self.name;

class Time:						# TODO
	name = "";
