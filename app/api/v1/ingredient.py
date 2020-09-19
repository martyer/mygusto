from flask import jsonify
from flask_cors import cross_origin
from flask_restplus import Namespace, Resource

from app.database.models import ShoppingList

ns = Namespace('ingredient')


@ns.route('/')
class IngredientResource(Resource):

    @cross_origin()
    def option(self):
        return 'Ok', 200

    @cross_origin()
    def get(self):
        """
        Get list of ingredients for a list of recipe
        """

        def get_shopping_list_recipe_ids() -> list:
            """
            Get the recipe ids in the shopping list

            :return: List of recipe ids
            """
            recipes = ShoppingList.query.all()
            return [recipe.recipe_id for recipe in recipes]

        def get_ingredients(recipe_ids: list) -> list:
            """
            Get the ingredients for the recipes in the shopping list

            :param recipe_ids: List of recipe ids in the shopping list
            :return: List of ingredients
            """
            # TODO: Insert code
            return recipe_ids

        recipe_ids = get_shopping_list_recipe_ids()
        ingredients = get_ingredients(recipe_ids)

        return jsonify(ingredients)
