from flask_cors import cross_origin
from flask_restplus import Namespace, Resource

ns = Namespace('ingredient')


@ns.route('/')
class IngredientResource(Resource):

    @cross_origin()
    def option(self):
        return 'Ok', 200

    @cross_origin()
    def get(self):
        """
        TODO
        """

        return
