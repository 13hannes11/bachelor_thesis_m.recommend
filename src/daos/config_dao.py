from daos.db import DB_CONFIG
from tinyrecord import transaction

from model.configuration_model import ConfigurationModel

class ConfigurationDAO:
    
    __instance = None
    def add(self, config):
        trans = DB_CONFIG()
        with transaction(trans) as tr:
            tr.insert(config)
    def getAll(self):
        return DB_CONFIG().all()
        
    def getAll_as_objects(self):
        configurations = []
        for conf in self.getAll():
            configurations.append(ConfigurationModel(conf))

    def exists(self, config):
        for conf in DB_CONFIG().all():
            if len(set(conf['configuration']).symmetric_difference(set(config['configuration']))) == 0:
                return True
        return False
    @staticmethod
    def getInstance():
        """ Static access method. """
        if ConfigurationDAO.__instance == None:
           ConfigurationDAO()
        return ConfigurationDAO.__instance
    def __init__(self):
        """ Virtually private constructor. """
        if ConfigurationDAO.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ConfigurationDAO.__instance = self

