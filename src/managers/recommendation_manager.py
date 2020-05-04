from daos.config_dao import ConfigurationDAO
from daos.product_structure_dao import ProductStructureDAO
from model.configuration_model import ConfigurationModel
from model.preferences_model import Preferences
from model.product_structure_model import ProductStructureModel
from scoring.scoring_functions import ReduceScoringFunctionFactory, ScoringFunction
import numpy as np
import operator

class RecommendationManager:
    def getRecommendation(self, preferences: Preferences , current_config : ConfigurationModel,
        scoring_methods = "avg",
        penalty_function = "penalty_ratio",
        product_structure = ProductStructureDAO.getInstance().get_as_objects(),
        configurations = ConfigurationDAO.getInstance().getAll()):
        avg = ReduceScoringFunctionFactory.build_scoring_function(
            [penalty_function, "pref_average_simpleSelectedCharacterstics_average"],
            product_structure,
            oper = operator.mul
        )
        lm = ReduceScoringFunctionFactory.build_scoring_function(
            [penalty_function, "pref_min_simpleSelectedCharacterstics_average"],
            product_structure,
            oper = operator.mul
        )
        multi = ReduceScoringFunctionFactory.build_scoring_function(
            [penalty_function, "pref_product_simpleSelectedCharacterstics_average"],
            product_structure,
            oper = operator.mul
        )

        default = SimpleConfigurationMaxSelector( avg )
        switcher = {
            "avg" : default,
            "multi": SimpleConfigurationMaxSelector(multi),
            "lm": SimpleConfigurationMaxSelector( lm ),
            "avg-lm": PipeFilterMax(ConfigurationFilter(avg), SimpleConfigurationMaxSelector( lm )),
            "lm-avg": PipeFilterMax(ConfigurationFilter(lm), SimpleConfigurationMaxSelector( avg ))
        }
        max_selector = switcher.get(scoring_methods, default)

        return max_selector.getMax(preferences, current_config, configurations)


class ConfigurationMaxSelector:
    def getMax(self, preferences: Preferences, current_config : ConfigurationModel, configurations):
        pass

class PipeFilterMax(ConfigurationMaxSelector):
    def __init__(self, configuration_filter : 'ConfigurationFilter', max_selector : ConfigurationMaxSelector):
        self.configuration_filter = configuration_filter
        self.max_selector = max_selector

    def getMax(self, preferences: Preferences, current_config : ConfigurationModel, configurations):
        list = self.configuration_filter.filter(preferences, current_config, configurations)
        return self.max_selector.getMax(preferences, current_config, list)
        

class ConfigurationFilter:
    def __init__(self, scoring_function : ScoringFunction, percentile = 50):
        assert percentile <= 100
        assert percentile >= 0
        self.scoring_function = scoring_function
        self.percentile = percentile
    def filter(self, 
        preferences: Preferences, 
        current_config : ConfigurationModel, 
        configurations):
        
        scores = list(map(lambda x: self.scoring_function.calc_score(current_config, preferences, ConfigurationModel(x)), configurations))
        
        barrier = np.percentile(np.array(scores), self.percentile)
        return list(filter(lambda x: self.scoring_function.calc_score(current_config, preferences, ConfigurationModel(x)) > barrier, configurations))
        
class SimpleConfigurationMaxSelector(ConfigurationMaxSelector):
    def __init__(self, scoring_function : ScoringFunction):
        self.scoring_function = scoring_function
    def getMax(self, preferences: Preferences, current_config : ConfigurationModel, configurations):
        best_rating = float("-inf")
        best = None

        for to_rate in configurations:
            score = self.scoring_function.calc_score(current_config, preferences, ConfigurationModel(to_rate))
            if score > best_rating:
                best = to_rate
                best_rating = score
        print('Best rating: {}'.format(best_rating))
        return best

