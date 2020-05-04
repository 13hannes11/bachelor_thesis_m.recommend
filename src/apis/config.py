from flask_restplus import Namespace, Resource, fields
from daos.config_dao import ConfigurationDAO

api = Namespace('config', description='Configuration related operations')

variable_model = api.model('config_variable', {
    'value': fields.Float(required=True, description='The contained variable value'),
    'code': fields.String(required=True, description='The contained variable code')
})

config_model = api.model('config', {
    'configuration': fields.List(fields.String(), required=True, description='The contained codes'),
    'variables': fields.List(fields.Nested(variable_model), required=True, description='The contained variables')
})

@api.route('/')
class ConfigList(Resource):

    @api.doc('list_configs')
    @api.marshal_list_with(config_model)
    def get(self):
        '''List all stored configurations'''
        return ConfigurationDAO.getInstance().getAll()

    @api.doc('add_config')
    @api.expect(config_model)
    @api.marshal_with(config_model, code=201)
    def post(self):
        '''Put configuration'''
        config = api.payload
        if not ConfigurationDAO.getInstance().exists(config):
            ConfigurationDAO.getInstance().add(api.payload)
        return api.payload, 201

    
