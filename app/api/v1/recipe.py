from flask import request, abort
from flask_restplus import Namespace, Resource, fields

from app.database import db
from app.database.models import LikedRecipes, DislikedRecipes

ns = Namespace('recipe')

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


@ns.route('/next')
class NextRecipeResource(Resource):

    @ns.expect(next_input)
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
            # TODO: insert code
            return {'seen_recipe_ids': seen_recipe_ids,
                    'gluten_intolerant': gluten_intolerant,
                    'lactose_intolerant': lactose_intolerant}

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
            # TODO: insert code
            return liked_recipe_ids

        liked_recipes_ids = get_liked_recipe_ids()
        liked_recipes = get_liked_recipes(liked_recipes_ids)

        return liked_recipes

    @ns.expect(liked_input)
    def post(self):
        def insert_element_into_db(recipe_id: int, sentiment: str):
            if sentiment == 'liked':
                new_recipe = LikedRecipes(recipe_id=recipe_id)
            elif sentiment == 'disliked':
                new_recipe = DislikedRecipes(recipe_id=recipe_id)
            else:
                abort(400, 'The sentiment must be either "liked" or "disliked".')

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

        return
