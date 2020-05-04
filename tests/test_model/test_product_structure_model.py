from model.product_structure_model import ProductStructureModel, ProductStructureElementModel, ProductStructureTypeEnum

class TestProductStructureModelEnum:
    def test_string_characteristic(self):
        assert ProductStructureTypeEnum['CHARACTERISTIC'] == ProductStructureTypeEnum.CHARACTERISTIC
    def test_string_cluster(self):
        assert ProductStructureTypeEnum['CLUSTER'] == ProductStructureTypeEnum.CLUSTER
    def test_string_variable(self):
        assert ProductStructureTypeEnum['VARIABLE'] == ProductStructureTypeEnum.VARIABLE
    def test_string_feature(self):
        assert ProductStructureTypeEnum['FEATURE'] == ProductStructureTypeEnum.FEATURE

class TestProductStructureElementModel:
    def test_get_list_of_all(self):
        data = {
            'elementId': 'parent',
            'name': 'parent_element',
            'type': "FEATURE",
            'additionalData': [],
            'children': [
                {
                    'elementId': 'child',
                    'name': 'child',
                    'children': [],
                    'additionalData': [],
                    'type': "CHARACTERISTIC"
                }
            ],
        }
        element = ProductStructureElementModel(data)
        assert len(element.get_list_of_all(ProductStructureTypeEnum.CHARACTERISTIC)) == 1

class TestProductStructureModel:
    def test_get_list_of_features(self):
        data = {
            'ProductStructure': [
                {
                    'elementId': 'parent',
                    'name': 'parent_element',
                    'type': "FEATURE",
                    'additionalData': [],
                    'children': [
                        {
                            'elementId': 'child',
                            'name': 'child',
                            'children': [],
                            'additionalData': [],
                            'type': "CHARACTERISTIC"
                        }
                    ],
                }
            ]
        }
        ps_structure = ProductStructureModel(data)
        assert len(ps_structure.get_list_of_features()) == 1
    def test_get_list_of_characteristics(self):
        data = {
            'ProductStructure': [
                {
                    'elementId': 'parent',
                    'name': 'parent_element',
                    'type': "FEATURE",
                    'additionalData': [],
                    'children': [
                        {
                            'elementId': 'child',
                            'name': 'child',
                            'children': [],
                            'additionalData': [],
                            'type': "CHARACTERISTIC"
                        }
                    ],
                }
            ]
        }
        ps_structure = ProductStructureModel(data)
        assert len(ps_structure.get_list_of_characteristics()) == 1
    def test_is_characteristic(self):
        data = {
            'ProductStructure': [
                {
                    'elementId': 'parent',
                    'name': 'parent_element',
                    'type': "FEATURE",
                    'additionalData': [],
                    'children': [
                        {
                            'elementId': 'child',
                            'name': 'child',
                            'children': [],
                            'additionalData': [],
                            'type': "CHARACTERISTIC"
                        }
                    ],
                }
            ]
        }
        ps_structure = ProductStructureModel(data)
        assert ps_structure.isCharacteristic('child') == True
        assert ps_structure.isCharacteristic('parent') == False