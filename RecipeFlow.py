from nltk import word_tokenize

allIngredients = ['chicken','water','butter','onion','chilies','seasoning'];
allCookActions = ['place','add','bring','reduce','cook','simmer','shred','combine','stir','turn','off','cover','heat'];
allUtensils = ['bag','heat','pot','skillet'];
allMeasurements = ['pieces','large','medium','low','medium-low','medium-high']

class RecipeFlowchart:
	allNodes = [];
	currentNode = None;
	firstNode = None;

	def __str__ (self):
		rv = ""
		for n in self.allNodes:
			rv += str(n);
		return rv;

	def __init__ (self):
		self.allNodes = [];

		# Cook Node
		cookAction = Node(allCookActions,"cook node");

		# Addition Node
		additionWordsAction = Node(['onto','with','together','each'], "addition node");
		cookAction.addNode(additionWordsAction);

		# Measurement Node 1
		measurements1Action = Node(allMeasurements, "0measurement");

		cookAction.addNode(measurements1Action);
		additionWordsAction.addNode(measurements1Action);

		# Ingredient Node 1

		ingredients1Action = Node(allIngredients, "0ingredient");

		ingredients1Action.addNode(ingredients1Action);
		ingredients1Action.addNode(measurements1Action);

		measurements1Action.addNode(ingredients1Action);
		cookAction.addNode(ingredients1Action);
		additionWordsAction.addNode(ingredients1Action);

		# Utensils Node 1
		uten1Action = Node(allUtensils, "0utensil");

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

		ingredients2Action.addNode(ingredients2Action);
		ingredients2Action.addNode(measurements2Action);

		measurements2Action.addNode(ingredients2Action);
		additionWords2Action.addNode(ingredients2Action);

		# Utensils Node 2
		uten2Action = Node(allUtensils, "1utensil");

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

		ingredients3Action.addNode(ingredients3Action);
		ingredients3Action.addNode(measurements3Action);

		measurements3Action.addNode(ingredients3Action);
		untilOverAction.addNode(ingredients3Action);

		# Utensils Node 3
		uten3Action = Node(allUtensils, "2utensil");

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

		self.firstNode = cookAction;
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

	def step (self, istring):

		# Only advance if the string is accepted as the next node or indicates the start of a new step
		for n in self.currentNode.nextNodes:
			if n.checkNode(istring):
				print(istring);
				self.currentNode = n;
				return;
		n = self.firstNode;
		if n.checkNode(istring):
			print("\nNew Step");
			print(istring);
			self.currentNode = n;
			return;

class Node:
	name = '';
	isTrueNode = False;
	values = '';
	nextNodes = [];

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

istring = "Place the chicken in a large pot and add water to cover. Bring to a boil over high heat, then reduce the heat to medium-low, cover, and simmer until the chicken pieces are no longer pink, about 10 minutes.";
istring = "Heat the butter in a skillet over medium heat. Stir in the onion; cook and stir until the onion has softened and turned translucent, about 5 minutes. Add the shredded chicken, chopped green chilies, taco seasoning, half of the bunch of chopped green onion, and water."

istring = istring.lower();
istring = word_tokenize(istring);
myrfc = RecipeFlowchart();

for i in istring:
		myrfc.step(i);

print(myrfc);