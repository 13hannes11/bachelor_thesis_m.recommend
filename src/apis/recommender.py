from flask_restplus import Namespace, Resource, fields
from .config import config_model
from managers.recommendation_manager import RecommendationManager
from model.configuration_model import ConfigurationModel
from model.preferences_model import Preferences

api = Namespace('recommender', description='Recommendation related operations')

rating_model = api.model('Rating', {
    'code': fields.String(required=True, description='The code that was rated'),
    'value': fields.Float(required=True, description='The rating value'),
})

preference_model = api.model('Preference', {
    'user': fields.String(required=True, description='The user identifier'),
    'ratings': fields.List(fields.Nested(rating_model),required=True, description='The list of ratings of this user'),
})

recommendation_request_model = api.model('Recommendation Request', {
    'configuration': fields.Nested(config_model, required=True, description='The user identifier'),
    'preferences': fields.List(fields.Nested(preference_model),required=True, description='The list of ratings of this user'),
})

@api.route('/')
class Recommendation(Resource):
    manager = RecommendationManager()
    @api.doc('get_recommendation')
    @api.expect(recommendation_request_model)
    @api.marshal_list_with(config_model)
    def post(self):
        '''Get recommendation'''
        result = self.manager.getRecommendation(Preferences(api.payload), ConfigurationModel(api.payload['configuration']))
        response = result
        return response



    
