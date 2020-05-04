from scoring.scoring_functions import PreferenceScoring, RatioCharacteristicConfigurationPenalty, WeightedFeaturePenalty, ReduceScoring
from scoring.value_functions import ValueToValueFunction
from model.configuration_model import ConfigurationModel
from model.preferences_model import Preferences
from scoring.list_functions import Min, Average
from scoring.preferences_functions import FlattenPreferencesToListFunction
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
currentConfiguration = ConfigurationModel({
    'configuration': ['A2', 'B2'],
    'variables': []
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

class TestRatioCharacteristicConfigurationPenalty:
    def test_simple_example(self):
        function = RatioCharacteristicConfigurationPenalty(product_structure, [ValueToValueFunction()])
        assert 0.5 == function.calc_score(currentConfiguration, preferences, toRate)


class TestWeightedFeaturePenalty:
    def test_simple_example(self):
        function = WeightedFeaturePenalty(product_structure, Min(), Average())
        assert 0.375 == function.calc_score(currentConfiguration, preferences, toRate)

class TestReduceScoring:
    def test_combined(self):
        function = ReduceScoring([
            RatioCharacteristicConfigurationPenalty(product_structure, [ValueToValueFunction()]),
            WeightedFeaturePenalty(product_structure, Min(), Average())
        ])
        assert 0.875 == function.calc_score(currentConfiguration, preferences, toRate)
    def test_none(self):
        function = ReduceScoring([])
        assert 0 == function.calc_score(currentConfiguration, preferences, toRate)

class TestPreferenceScoring:
    def test_simple_example(self):
        function = PreferenceScoring(
            FlattenPreferencesToListFunction(), 
            Min()
        )
        assert 0 == function.calc_score(currentConfiguration, preferences, toRate)

