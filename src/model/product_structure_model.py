from typing import List
from enum import Enum

class ProductStructureTypeEnum(Enum):
    CHARACTERISTIC = "CHARACTERISTIC",
    FEATURE = "FEATURE",
    CLUSTER = "CLUSTER",
    VARIABLE = "VARIABLE",


class ProductStructureElementModel:
    def __init__(self, data):
        self.children = []
        self.type = None
        self.elementId = data['elementId']
        self.type = data['type']
        self.name = data['name']
        self.additionalData = data['additionalData']

        for element in data['children']:
            self.children.append(ProductStructureElementModel(element))

    def get_list_of_all(self, type : ProductStructureTypeEnum) :
        tmp_list = []
        for child in self.children :
            tmp_list = tmp_list + child.get_list_of_all(type)
        if ProductStructureTypeEnum[self.type] == type:
            tmp_list.append(self)
        return tmp_list

    def get_children_characteristics(self):
        tmp_list = self.get_list_of_all(ProductStructureTypeEnum.CHARACTERISTIC)
        if self in tmp_list:
            tmp_list.remove(self)
        return tmp_list


class ProductStructureModel:
    list_of_features = []
    list_of_characteristics = []
    def __init__(self, data):
        self.productStructure : List[ProductStructureElementModel] = []
        for element in data['ProductStructure']:
            child = ProductStructureElementModel(element)
            self.productStructure.append(child)
    
    def get_list_of_features(self):
        if (self.list_of_features == []) :
            tmp_list = []
            for element in self.productStructure:
                tmp_list = tmp_list + element.get_list_of_all(ProductStructureTypeEnum.FEATURE)
            self.list_of_features = tmp_list
        
        return self.list_of_features
    
    def get_list_of_characteristics(self):
        if (self.list_of_features == []) :
            tmp_list = []
            for element in self.productStructure:
                tmp_list = tmp_list + element.get_list_of_all(ProductStructureTypeEnum.CHARACTERISTIC)
            self.list_of_characteristics = tmp_list
        
        return self.list_of_characteristics

    def isCharacteristic(self, code: str) -> bool:
        list = self.get_list_of_characteristics()
        return any(map(lambda x: x.elementId == code , list))



    