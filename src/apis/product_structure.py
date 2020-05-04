from flask_restplus import Namespace, Resource, fields
from daos.product_structure_dao import ProductStructureDAO
import copy

api = Namespace('product_structure', description='Product structure related operations')

product_structure_model = api.model('Product Structure', {
    #'ProductStructure': fields.List(fields.Wildcard(), required=True, example="{}", description='The array containing the product structure elements'),
})

DAO = ProductStructureDAO.getInstance()

@api.route('/')
class ProductStructure(Resource):
    @api.doc('show_product_structure')
    #@api.marshal_list_with(product_structure_model)
    def get(self):
        '''Return product structure'''
        return DAO.get()

    @api.doc('replace_product_structure')
    @api.expect(product_structure_model)
    #@api.marshal_with(product_structure_model, code=201)
    def put(self):
        '''replace product structure'''
        DAO.replace(api.payload)
        return DAO.get(), 201

    
