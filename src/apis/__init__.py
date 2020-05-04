from flask_restplus import Api

from .config import api as config_api
from .recommender import api as recommender_api
from .product_structure import api as prod_structure_api

api = Api(
    title='Configuration Recommendation API',
    version='1.0',
    description='A simple recommendation API',
)

api.add_namespace(recommender_api)
api.add_namespace(config_api)
api.add_namespace(prod_structure_api)