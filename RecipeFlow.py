from nltk import word_tokenize
from RecipeStructure import Recipe, Step, Action, Ingredient, Utensil, Time

allIngredients = ['cream','cheese','ham','chicken','water','butter','onion','chilies','seasoning','breast','filling','flour','paprika','wine','bouillon','juices'];
allCookActions = ['pound','place','add','bring','reduce','cook','simmer','shred','combine','stir','turn','off','cover','heat','fold','secure','coat','mix','reduce','transfer'];
allUtensils = ['bag','heat','pot','skillet','bowl','platter'];
allMeasurements = ['pieces','large','medium','low','medium-low','medium-high','slice','small','pieces']
allConditions = ['medium-low','pink','softened','translucent','low','medium','high','clear']

class RecipeFlowchart:
	allNodes = [];
	currentNode = None;
	firstNode = None;
	myrecipe = Recipe();
	stringbuffer = "";

	def __str__ (self):
		rv = ""
		for n in self.allNodes:
			rv += str(n);
		return rv;

	def __init__ (self):
		stringbuffer = "";

		self.myrecipe = Recipe();
		self.startNewRecipeStep("");
		self.allNodes = [];

		firstNode = Node([""],"first node");
		firstNode.action = "startNewRecipeStep";

		# Cook Node
		cookAction = Node(allCookActions,"cook action");
		cookAction.action = "addAction";

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
		self.firstNode = firstNode;
		self.currentNode = self.firstNode;

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
				n.doAction(self, self.stringbuffer);
				self.currentNode = n;
				if not "measure" in n.name:
					self.stringbuffer = "";
				#print(istring + " " + n.name);
				return;

		for n in self.firstNode.nextNodes:
			if n.checkNode(istring):
				self.firstNode.doAction(self, self.stringbuffer);
				self.stringbuffer = istring;

				#print("\n\nNew Step");
				n.doAction(self, self.stringbuffer);
				self.stringbuffer = "";
				self.currentNode = n;
				return;
		return;

	def startNewRecipeStep (self, iname):
		self.myrecipe.addStep(Step("stepName"));

	def addAction (self, iname):
		myaction = Action(iname);
		self.myrecipe.getLastStep().addAction(myaction);

	def addIngredient (self, iname):
		myingred = Ingredient(iname);
		self.myrecipe.getLastStep().addIngredient(myingred);

	def addUtensil (self, iname):
		myuten = Utensil(iname);
		self.myrecipe.getLastStep().addUtensil(myuten);

	def addCondition (self, iname):
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
				recipe.addAction(parameter);
			if self.action == "addIngredient":
				recipe.addIngredient(parameter);
			if self.action == "addUtensil":
				recipe.addUtensil(parameter);
			if self.action == "addCondition":
				recipe.addCondition(parameter);

istring = "Place the chicken in a large pot and add water to cover. Bring to a boil over high heat, then reduce the heat to medium-low, cover, and simmer until the chicken pieces are no longer pink, about 10 minutes.";
#istring = "Heat the butter in a skillet over medium heat. Stir in the onion; cook and stir until the onion has softened and turned translucent, about 5 minutes. Add the shredded chicken, chopped green chilies, taco seasoning, half of the bunch of chopped green onion, and water."
#istring = "Pound chicken breasts if they are too thick. Place a cheese and ham slice on each breast within 1/2 inch of the edges. Fold the edges of the chicken over the filling, and secure with toothpicks. Mix the flour and paprika in a small bowl, and coat the chicken pieces. Heat the butter in a large skillet over medium-high heat, and cook the chicken until browned on all sides. Add the wine and bouillon. Reduce heat to low, cover, and simmer for 30 minutes, until chicken is no longer pink and juices run clear. Remove the toothpicks, and transfer the breasts to a warm platter. Blend the cornstarch with the cream in a small bowl, and whisk slowly into the skillet. Cook, stirring until thickened, and pour over the chicken. Serve warm."

istring = istring.lower();
istring = word_tokenize(istring);
myrfc = RecipeFlowchart();

for i in istring:
	myrfc.step(i);

print(myrfc.myrecipe);

#print(myrfc);