from nltk import word_tokenize, sent_tokenize
from RecipeStructure import Recipe, Step, Ingredient, Action

sometext = "In a large pot of salted boiling water, cook angel hair pasta until it is al dente, about 8 to 10 minutes. Drain, and set aside.\nIn a large skillet, heat oil over medium-high heat. Saute the onions and garlic. Stir in the tomatoes, chicken, basil, salt and hot pepper sauce. Reduce heat to medium, and cover skillet. Simmer for about 5 minutes, stirring frequently, until mixture is hot and tomatoes are soft.\nToss sauce with hot cooked angel hair pasta to coat. Serve with Parmesan cheese."
iList = ['salted boiling water','angel hair pasta','oil','onions','garlic','tomatoes','chicken','basil','salt','hot pepper sauce','parmesan cheese'];
aList = ['cook','drain','heat','saute','stir','simmer','toss','serve'];
uList = ['pot','skillet'];

print(RecipeParse.parseRecipe(sometext));

class RecipeParse:
	def parseRecipe (self, itext):
		myRecipe = Recipe();
		sentence = nltk.sent_tokenize(itext);
		for i in sentence:
			myRecipe.addStep(parseStep(i));


class StepParse:
	def parseStep (self, itext):
		thisStep = Step();

		words = nltk.word_tokenize(itext);
		for w in words:
			if w.lower() in iList:
				thisStep.addIngredient(Ingredient(w));
			if w.lower() in aList:
				thisStep.addAction(Action(w));

		return thisStep;
