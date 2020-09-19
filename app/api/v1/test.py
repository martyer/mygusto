from flask_restplus import Namespace, Resource

ns = Namespace('test')


@ns.route('/')
class TestResource(Resource):
    def get(self):
        """
        This is a test
        """

        return "Hello World"
