from daos.db import DB_PRODUCT_STRUCTURE
from tinydb import Query
from tinyrecord import transaction

from model.product_structure_model import ProductStructureModel

rmList = []

class ProductStructureDAO(object):
    __instance = None

    def get_as_objects(self) -> ProductStructureModel:
        return ProductStructureModel(self.get())

    def get(self):
        highest_id = self._get_highest_id()
        return DB_PRODUCT_STRUCTURE().get(doc_id=highest_id)

    def replace(self, structure):
        highest_id = self._get_highest_id()
        rmList = list(range(0,highest_id + 1))
        trans = DB_PRODUCT_STRUCTURE()
        with transaction(trans) as tr:
            tr.insert(structure)
            tr.remove(doc_ids=rmList)
        return structure
    def _get_highest_id(self):
        all = DB_PRODUCT_STRUCTURE().all()
        max = 0
        for element in all:
            if element.doc_id > max:
                max = element.doc_id
        return max

    @staticmethod
    def getInstance():
        """ Static access method. """
        if ProductStructureDAO.__instance == None:
           ProductStructureDAO()
        return ProductStructureDAO.__instance
    def __init__(self):
        """ Virtually private constructor. """
        if ProductStructureDAO.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ProductStructureDAO.__instance = self
    
        