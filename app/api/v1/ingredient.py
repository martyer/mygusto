from flask_restplus import Namespace, Resource

ns = Namespace('ingredient')


@ns.route('/')
class IngredientResource(Resource):

    def get(self):
        """
        TODO
        """

        return
