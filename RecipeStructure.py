class Recipe:
	firstStep = None;			# The first step in our recipe. A Step object

	def __init__(self):		# Constructor
		self.firstStep = None;

	def __str__ (self):
		rv = "";
		currentStep = self.firstStep;
		while currentStep != None:
			rv += str(currentStep);
			currentStep = currentStep.nextStep;
		rv += self.getJSON();
		return rv;

	def getJSON (self):
		rv = "{\"steps\": [";
		lastStep = self.firstStep;
		while not lastStep.nextStep == None:
			rv += lastStep.getJSON() + ",";
			lastStep = lastStep.nextStep;
		rv += "]}";
		return rv;

	def addStep(self, inputStep):			# Build the recipes by adding steps to the end
		if self.firstStep == None:
			self.firstStep = inputStep;
		else:
			lastStep = self.firstStep;
			while lastStep.nextStep != None:
				lastStep = lastStep.nextStep;
			inputStep.StepNumber = lastStep.StepNumber + 1;
			lastStep.nextStep = inputStep;

	def getLastStep (self):
		lastStep = self.firstStep;
		while not lastStep.nextStep == None:
			lastStep = lastStep.nextStep;
		return lastStep;

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
			rv += "Ingredients: \n";
		for i in self.ingredients:
			rv += "\t" + str(i) + "\n";
		if len(self.actions) > 0:
			rv += "Actions: \n"
		for a in self.actions:
			rv += "\t" + str(a) + "\n";
		if not self.unassigneduten == None:
			rv += "Utensil: \n"
			rv += "\t" + str(self.unassigneduten) + "\n";
		if len(self.time) > 0:
			rv += "Time: \n";
		for t in self.time:
			rv += "\t" + str(t) + "\n";
		return rv + "\n";

	def getJSON (self):
		rv = "{\"ingredients\": [";
		for i in self.ingredients:
			rv += i.getJSON() + ",";
		rv += "],";
		rv += "\"cooking method\": [";
		for a in self.actions:
			rv += "\"" + a.name + "\",";
		rv += "],";
		rv += "\"cooking tools\": [";
		for a in self.actions:
			if a.utensil != None:
				rv += "\"" +  a.utensil.name + "\"";
		rv += "],}";
		return rv;



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
		return self.name;

	def getJSON (self):
		rv = "{";
		rv += "\"name\": \"" + self.name + "\",";
		rv += "\"quantity\": \"" + str(self.quantity) + "\",";
		rv += "\"measurement\": \"" + str(self.unit) + "\",";
		rv += "\"descriptor\": \"" + self.descriptor + "\",";
		#rv += "\"preparation\": \"" + str(self.form) + "\"}";
		return rv;

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
		return self.name;

class Time:						# TODO
	name = "";

	def __init__ (self, iname):
		self.name = iname;

	def __str__ (self):
		return self.name;
