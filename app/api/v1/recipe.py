from time import sleep

from elasticsearch import Elasticsearch, TransportError
from flask import request, abort, jsonify
from flask_cors import cross_origin
from flask_restplus import Namespace, Resource, fields

from app.database import db
from app.database.models import LikedRecipes, DislikedRecipes, ShoppingList, FeatureVectors
from app.utils.recipe_parser import extract_recipe_info

ns = Namespace('recipe')

es = Elasticsearch(
    ['https://hackzurich-api.migros.ch/hack/recipe/recipes_de/_search'],
    http_auth=('hackzurich2020', 'uhSyJ08KexKn4ZFS')
)

next_input = ns.model('next_input', {
    'gluten_intolerant': fields.Boolean(
        required=True,
        description='Whether the user is intolerant to gluten',
        example=0
    ),
    'lactose_intolerant': fields.Boolean(
        required=True,
        description='Whether the user is intolerant to lactose',
        example=0
    )
})

liked_input = ns.model('liked_input', {
    'recipe_id': fields.Integer(
        required=True,
        description='The recipe id for the (dis)-liked recipe',
        example=23221
    ),
    'sentiment': fields.String(
        required=True,
        description='Whether the user liked or disliked the recipe ["liked", "disliked"]',
        example='liked'
    )
})

shopping_list_input = ns.model('shopping_list_input', {
    'recipe_id': fields.Integer(
        required=True,
        description='The recipe id for the recipe that will be added to the shopping list',
        example=23221
    )
})


@ns.route('/next')
class NextRecipeResource(Resource):

    @cross_origin()
    def option(self):
        return 'Ok', 200

    @ns.expect(next_input)
    @cross_origin()
    def post(self):
        """
        Get next recipe to be swiped
        """

        def get_liked_recipe_ids() -> list:
            """
            Get the list of recipe ids that the user liked

            :return: List of recipe ids
            """
            recipes = LikedRecipes.query.all()
            return [recipe.recipe_id for recipe in recipes]

        def get_disliked_recipe_ids() -> list:
            """
            Get the list of recipe ids that the user disliked

            :return: List of recipe ids
            """
            recipes = DislikedRecipes.query.all()
            return [recipe.recipe_id for recipe in recipes]

        def get_next_recipe(seen_recipe_ids: list, gluten_intolerant: bool, lactose_intolerant: bool) -> dict:
            """
            Get the next recipe to display

            :param seen_recipe_ids: List of already swiped recipe ids
            :param gluten_intolerant: Whether the user is gluten intolerant
            :param lactose_intolerant: Whether the user is lactose intolerant
            :return: Dictionary of the next recipe
            """

            next_recipe = None
            for i in range(5):
                params = {
                    'size': 20,
                    'query': {
                        'function_score': {
                            'random_score': {},
                        }
                    }
                }
                rand_request = None
                for j in range(3):
                    try:
                        rand_request = es.search(index='recipes_de', body=params)
                    except TransportError:
                        sleep(0.1)
                if not rand_request:
                    abort(500, 'Migros API is busy, please try again later.')

                new_recipes = [recipe for recipe in rand_request['hits']['hits'] if
                               int(recipe['_source']['id']) not in seen_recipe_ids]

                for recipe in new_recipes:
                    if gluten_intolerant and 'Glutenfrei' not in [tag['name'] for tag in recipe["_source"]["tags"]]:
                        continue
                    if lactose_intolerant and 'Laktosefrei' not in [tag['name'] for tag in recipe["_source"]["tags"]]:
                        continue
                    next_recipe = recipe
                    break

                if next_recipe:
                    break

            if not next_recipe:
                raise Exception('No recipe found')

            return extract_recipe_info(next_recipe)

        data = request.json

        if data is None:
            abort(400, 'No JSON payload found. Please make sure to pass a body and set '
                       '"Content-Type: application/json" header.')

        if 'gluten_intolerant' not in data:
            abort(400, 'Please supply the key "gluten_intolerant" in the input JSON.')

        if 'lactose_intolerant' not in data:
            abort(400, 'Please supply the key "lactose_intolerant" in the input JSON.')

        gluten_intolerant = bool(data['gluten_intolerant'])
        lactose_intolerant = bool(data['lactose_intolerant'])

        seen_recipe_ids = get_liked_recipe_ids()
        seen_recipe_ids.extend(get_disliked_recipe_ids())

        next_recipe = get_next_recipe(seen_recipe_ids, gluten_intolerant, lactose_intolerant)

        return next_recipe


@ns.route('/liked')
class LikedRecipeResource(Resource):

    @cross_origin()
    def option(self):
        return 'Ok', 200

    @cross_origin()
    def get(self):
        """
        Handle liked recipes
        """

        def get_liked_recipe_ids() -> list:
            """
            Get the list of recipe ids that the user liked

            :return: List of recipe ids
            """
            recipes = LikedRecipes.query.all()
            return [recipe.recipe_id for recipe in recipes]

        def get_liked_recipes(liked_recipe_ids: list) -> list:
            """
            Get a list of recipe information for the user liked recipes

            :param liked_recipe_ids: List of recipe ids
            :return: List of dictionaries of recipes
            """
            params = {
                "query": {
                    "ids": {
                        "values": liked_recipe_ids
                    }
                }
            }
            indexes_request = None
            for j in range(3):
                try:
                    indexes_request = es.search(index='recipes_de', body=params)
                except TransportError:
                    sleep(0.1)
            if not indexes_request:
                abort(500, 'Migros API is busy, please try again later.')

            recipes = indexes_request['hits']['hits']

            return [extract_recipe_info(recipe) for recipe in recipes]

        liked_recipes_ids = get_liked_recipe_ids()
        liked_recipes = get_liked_recipes(liked_recipes_ids)

        return jsonify(liked_recipes)

    @ns.expect(liked_input)
    @cross_origin()
    def post(self):
        """
        Add a new (dis)-liked recipe
        """

        def insert_element_into_db(recipe_id: int, sentiment: str) -> None:
            """
            Insert recipe id into corresponding sentiment table

            :param recipe_id: Id of a swiped recipe
            :param sentiment: String containing info if the recipe was swiped left or right
            :return: None
            """

            def create_feature_vector(recipe_id: int) -> str:
                """
                Create feature vector for KNN classification

                :param recipe_id: Id of a swiped recipe
                :return: JSON representation of feature vector
                """
                return 'test'

            if sentiment == 'liked':
                new_recipe = LikedRecipes(recipe_id=recipe_id)

            elif sentiment == 'disliked':
                new_recipe = DislikedRecipes(recipe_id=recipe_id)
            else:
                abort(400, 'The sentiment must be either "liked" or "disliked".')

            features = create_feature_vector(recipe_id)
            new_feature = FeatureVectors(features=features, sentiment=sentiment)
            db.session.add(new_feature)
            db.session.add(new_recipe)
            db.session.commit()

        data = request.json

        if data is None:
            abort(400, 'No JSON payload found. Please make sure to pass a body and set '
                       '"Content-Type: application/json" header.')

        if 'recipe_id' not in data:
            abort(400, 'Please supply the key "recipe_id" in the input JSON.')

        if 'sentiment' not in data:
            abort(400, 'Please supply the key "sentiment" in the input JSON.')

        recipe_id = data['recipe_id']
        sentiment = data['sentiment']

        insert_element_into_db(recipe_id, sentiment)

        return ''


@ns.route('/shopping_list')
class ShoppingListResource(Resource):

    @cross_origin()
    def option(self):
        return 'Ok', 200

    @ns.expect(shopping_list_input)
    @cross_origin()
    def post(self):
        """
        Add a new recipe to the shopping list
        """

        def insert_element_into_shopping_list(recipe_id: int) -> None:
            """
            Insert recipe into shopping list table

            :param recipe_id: Id of recipe to be inserted into the shopping list
            :return: None
            """
            recipe = ShoppingList(recipe_id=recipe_id)
            db.session.add(recipe)
            db.session.commit()

        data = request.json

        if data is None:
            abort(400, 'No JSON payload found. Please make sure to pass a body and set '
                       '"Content-Type: application/json" header.')

        if 'recipe_id' not in data:
            abort(400, 'Please supply the key "recipe_id" in the input JSON.')

        recipe_id = data['recipe_id']

        insert_element_into_shopping_list(recipe_id)

        return ''

    @cross_origin()
    def delete(self):
        """
        Clear shopping list
        """

        def clear_shopping_list() -> None:
            """
            Deletes all elements in shopping list table

            :return: None
            """
            ShoppingList.query.delete()
            db.session.commit()

        clear_shopping_list()

        return ''
