from flask import jsonify
from flask_cors import cross_origin
from flask_restplus import Namespace, Resource
from elasticsearch import Elasticsearch


from app.database.models import ShoppingList

ns = Namespace('ingredient')

es = Elasticsearch(
    ['https://hackzurich-api.migros.ch/hack/recipe/recipes_de/_search'],
    http_auth=('hackzurich2020', 'uhSyJ08KexKn4ZFS'))

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
            params = {"query": {
                "ids": {
                    "values": recipe_ids
                }
            }
            }
            indxs_request = es.search(index='recipes_de', body=params)
            recipes = indxs_request['hits']['hits']

            ingredients = {}
            ingredients['test'] = 'hi'
            for recipe in recipes:
                factor = 1
                recipe = recipe['_source']
                size = recipe['available_sizes'][0]
                if size != 2:
                    factor = size / 2
                for ingredient in recipe['sizes'][0]['ingredient_blocks'][0]['ingredients']:
                    if ingredient['text'] in ingredients:
                        ingredients[ingredient['text']]['amount'] += ingredient['amount']['quantity'] / factor
                    else:
                        ingredients[ingredient['text']] = {}
                        ingredients[ingredient['text']]['amount'] = ingredient['amount']['quantity'] / factor
                        ingredients[ingredient['text']]['unit'] = ingredient['amount']['unit']

            return ingredients

        recipe_ids = get_shopping_list_recipe_ids()
        ingredients = get_ingredients(recipe_ids)

        return jsonify(ingredients)
