from typing import List
from functools import reduce
import operator 

from model.preferences_model import Preferences
from model.configuration_model import ConfigurationModel

from scoring.list_functions import ListToListFunction, ListToValueFunction, Average, Min, Product
from scoring.preferences_functions import PreferencesToListFunction, FlattenPreferencesToListFunction, SimplePerUserToListFunction, PerUserPerFeatureDistanceAverageToListFunction, SimpleSelectedCharacteristicsToListFunction
from scoring.value_functions import ValueToValueFunction, MapToPercent, PowerFunction
from model.product_structure_model import ProductStructureModel

class ScoringFunctionFactory:
    @staticmethod
    def build_scoring_function(params : List[str]) -> 'ScoringFunction':
        pass

class ReduceScoringFunctionFactory(ScoringFunctionFactory):
    @staticmethod
    def build_scoring_function(params : List[str], product_structure : ProductStructureModel, oper = operator.add) -> 'SumScoring':
        list = []

        for param in params:
            switcher = {
                "penalty_ratio" : RatioCharacteristicConfigurationPenalty(product_structure, [PowerFunction(0.5)]),
                "penealty_average_weightedFeature_average": WeightedFeaturePenalty(
                    product_structure, 
                    Average(),
                    Average()
                    ),
                "pref_average_flat":  PreferenceScoring(
                    FlattenPreferencesToListFunction(), 
                    Average()
                ),
                "pref_average_perUser_Average": PreferenceScoring(
                    SimplePerUserToListFunction(Average()),
                    Average()
                ),
                "pref_average_simpleSelectedCharacterstics_average": PreferenceScoring(
                    SimpleSelectedCharacteristicsToListFunction(Average()),
                    Average()
                ),
                "pref_min_simpleSelectedCharacterstics_average": PreferenceScoring(
                    SimpleSelectedCharacteristicsToListFunction(Average()),
                    Min()
                ),
                "pref_product_simpleSelectedCharacterstics_average": PreferenceScoring(
                    SimpleSelectedCharacteristicsToListFunction(Average()),
                    Product()
                ),
                "pref_min_perUserPerFeatureDistance_average" : PreferenceScoring(
                    PerUserPerFeatureDistanceAverageToListFunction(Average(), product_structure),
                    Min()
                ),
                "pref_average_perUserPerFeatureDistance_average" : PreferenceScoring(
                    PerUserPerFeatureDistanceAverageToListFunction(Average(), product_structure),
                    Average()
                )
            }
            value = switcher.get(param, None)
            if value != None:
                list.append(value)
        
        return ReduceScoring(list, reduce_operator=oper)


class ScoringFunction:
    def calc_score(self, currentConfiguration : ConfigurationModel, preferences : Preferences, toRate : ConfigurationModel) -> float:
        pass

class PreferenceScoring(ScoringFunction):
    def __init__(self, preferenceToList : PreferencesToListFunction, listToValue : ListToValueFunction, listToList: List[ListToListFunction] = [], valueToValue: List[ValueToValueFunction] = []): 
        self.preferenceToListFunction = preferenceToList
        self.listToValueFunction = listToValue
        self.listToListFunctions = listToList
        self.valueToValueFunctions = valueToValue

    def calc_score(self, currentConfiguration : ConfigurationModel, preferences : Preferences, toRate : ConfigurationModel) -> float:
        list : List[float] = self.preferenceToListFunction.convertToList(preferences, toRate)

        for function in self.listToListFunctions : 
            list = function.applyToList(list)
        
        value = self.listToValueFunction.convertToFloat(list)

        for function in self.valueToValueFunctions :
            value = function.applyToValue(value)
        
        return value

class ConfigurationPenalty(ScoringFunction):
    def calc_score(self, currentConfiguration : ConfigurationModel, preferences : Preferences, toRate : ConfigurationModel) -> float:
        pass

class RatioCharacteristicConfigurationPenalty(ConfigurationPenalty):
    def __init__(self, product_structure : ProductStructureModel, valToValFunctions : List[ValueToValueFunction]):
        self.product_structure = product_structure
        self.valToValFunctions = valToValFunctions

    def calc_score(self, currentConfiguration : ConfigurationModel, preferences : Preferences, toRate : ConfigurationModel) -> float:
        inCount : float = 0
        charCount : float = 0
        for code in currentConfiguration.configuration:
            if self.product_structure.isCharacteristic(code):
                charCount += 1
                if code in toRate.configuration:
                    inCount += 1
        if charCount > 0:
            res = inCount / charCount
        else :
            res = 1

        for function in self.valToValFunctions:
            res = function.applyToValue(res)
        return res 

class WeightedFeaturePenalty(ScoringFunction):
    def __init__(self, product_structure : ProductStructureModel, per_feature_aggregation : ListToValueFunction, per_feature_per_user_aggregation : ListToValueFunction):
        self.product_structure = product_structure
        self.feature_aggregation = per_feature_aggregation
        self.user_aggregation = per_feature_per_user_aggregation
    
    def calc_score(self, currentConfiguration : ConfigurationModel, preferences : Preferences, toRate : ConfigurationModel) -> float:
        features = self.product_structure.get_list_of_features()
        
        feature_scores = []
        for feature in features:
            code_in_current = None
            code_in_to_rate = None
            for characteristic in feature.children:
                if characteristic.elementId in currentConfiguration.configuration :
                    code_in_current = characteristic.elementId
                if characteristic.elementId in toRate.configuration:
                    code_in_to_rate = characteristic.elementId
            users = preferences.getAllUsers()
            
            if code_in_current == None:
                break
            if code_in_current == code_in_to_rate:
                feature_scores.append(1)
            else:
                user_scores = []
                for user in users:
                    rating_to_rate =  preferences.getRatingValueByUserAndCode(user, code_in_to_rate)
                    rating_current = preferences.getRatingValueByUserAndCode(user, code_in_current)
                    user_scores.append(rating_to_rate - rating_current)
                feature_scores.append(self.user_aggregation.convertToFloat(user_scores))
        map_to_percent = MapToPercent(1, -1)
        return map_to_percent.applyToValue(self.feature_aggregation.convertToFloat(feature_scores)) 


class ReduceScoring(ScoringFunction):
    def __init__(self, scoringFunctions : List[ScoringFunction], reduce_operator = operator.add):
        self.scoringFunctions = scoringFunctions
        self.reduce_operator = reduce_operator
    def calc_score(self, currentConfiguration : ConfigurationModel, preferences : Preferences, toRate : ConfigurationModel) -> float:
        if len(self.scoringFunctions) > 0:
            score = reduce(self.reduce_operator, map(lambda x: x.calc_score(currentConfiguration, preferences, toRate), self.scoringFunctions))
            return score
        else:
            return 0

