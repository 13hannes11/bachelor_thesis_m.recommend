from scoring.preferences_functions import PerUserPerFeatureDistanceAverageToListFunction, SimplePerUserToListFunction, PreferencesToListFunction, FlattenPreferencesToListFunction
from scoring.list_functions import Min
from model.configuration_model import ConfigurationModel
from model.preferences_model import Preferences
from model.product_structure_model import ProductStructureModel

preferences = Preferences({
        'preferences': [
            {
                'user': "user0",
                'ratings':[ {
                        'code': 'A1',
                        'value': 0
                    }, {
                        'code': 'A2',
                        'value': 1
                    }, {
                        'code': 'B1',
                        'value': 0.5
                    }
                ]
            },
            {
                'user': "user1",
                'ratings':[ {
                        'code': 'A1',
                        'value': 1
                    }, {
                        'code': 'B2',
                        'value': 1
                    }
                ]
            }
        ]
    })
toRate = ConfigurationModel({
    'configuration': ['A1', 'B2'],
    'variables': []
})

product_structure = ProductStructureModel({
    'ProductStructure': [
            {
                'elementId': 'A',
                'name': 'parent_element A',
                'type': "FEATURE",
                'additionalData': [],
                'children': [
                    {
                        'elementId': 'A1',
                        'name': 'child A1',
                        'children': [],
                        'additionalData': [],
                        'type': "CHARACTERISTIC"
                    },
                                        {
                        'elementId': 'A2',
                        'name': 'child A2',
                        'children': [],
                        'additionalData': [],
                        'type': "CHARACTERISTIC"
                     }
                ],
            },{
                'elementId': 'B',
                'name': 'parent_element B',
                'type': "FEATURE",
                'additionalData': [],
                'children': [
                    {
                        'elementId': 'B1',
                        'name': 'child B1',
                        'children': [],
                        'additionalData': [],
                        'type': "CHARACTERISTIC"
                    },
                                        {
                        'elementId': 'B2',
                        'name': 'child B2',
                        'children': [],
                        'additionalData': [],
                        'type': "CHARACTERISTIC"
                     }
                ],
            },
        ]
    })
def float_lists_same(first, second):
    for element in first:
        if element not in second:
            return False
        second.remove(element)
    if len(second) != 0:
        return False
    return True
class TestPreferencesToListFunction:
    def test_should_be_empty_list(self):
        function = PreferencesToListFunction()
        assert len(function.convertToList(preferences, toRate)) == 0

class TestFlattenPreferencesToListFunction():
    def test_simple_example(self):
        function = FlattenPreferencesToListFunction()
        assert float_lists_same([1.0,0.5,0.0,0.0,1.0], function.convertToList(preferences, toRate))

class TestSimplePerUserToListFunction():
    def test_simple_example(self):
        function = SimplePerUserToListFunction(Min())
        assert float_lists_same([0.0, 1.0], function.convertToList(preferences, toRate))

class TestPerUserPerFeatureDistanceAverageToListFunction():
    def test_simple_example(self):
        function = PerUserPerFeatureDistanceAverageToListFunction(Min(), product_structure)
        assert float_lists_same([0.25, 0.625], function.convertToList(preferences, toRate))