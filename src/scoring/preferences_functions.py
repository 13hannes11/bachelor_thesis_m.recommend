from typing import List
from model.preferences_model import Preferences, Rating
from model.configuration_model import ConfigurationModel
from model.product_structure_model import ProductStructureModel

from scoring.list_functions import ListToValueFunction
from scoring.value_functions import MapToPercent

class PreferencesToListFunction:
    def convertToList(self, preferences : Preferences, toRate : ConfigurationModel) -> List[float]:
        return []

class FlattenPreferencesToListFunction(PreferencesToListFunction):
    def convertToList(self, preferences : Preferences, toRate : ConfigurationModel) -> List[float]:
        list : List[Rating] = []
        for user_pref in preferences.getAllUserPreferences():
            for rating in user_pref.getAllRatings():
                if rating.code in toRate.configuration:
                    list.append(rating.getValue())
                else :
                    list.append(1 - rating.getValue())
        return list

class SimplePerUserToListFunction(PreferencesToListFunction):
    def __init__(self, listToValue : ListToValueFunction):
        self.listToValueFunction = listToValue
    
    def convertToList(self, preferences : Preferences, toRate : ConfigurationModel) -> List[float]:
        list = []
        for user_pref in preferences.getAllUserPreferences():
            user_list : List[float] = []
            for rating in user_pref.getAllRatings():
                if rating.code in toRate.configuration:
                    user_list.append(rating.getValue())
                else :
                    user_list.append(1 - rating.getValue())
            list.append(self.listToValueFunction.convertToFloat(user_list))
        return list

class SimpleSelectedCharacteristicsToListFunction(PreferencesToListFunction):
    def __init__(self, listToValue : ListToValueFunction):
        self.listToValueFunction = listToValue

    def convertToList(self, preferences : Preferences, toRate : ConfigurationModel) -> List[float]:
        list = []
        for user_pref in preferences.getAllUserPreferences():
            user_list : List[float] = []
            for code in toRate.configuration:
                user_list.append(user_pref.getRatingByCode(code).getValue())
            list.append(self.listToValueFunction.convertToFloat(user_list))
        return list
class PerUserPerFeatureDistanceAverageToListFunction(PreferencesToListFunction):
    def __init__(self, featureListToValue : ListToValueFunction, product_structure : ProductStructureModel):
        self.featureListToValueFunction = featureListToValue
        self.product_structure = product_structure

    def convertToList(self, preferences : Preferences, toRate : ConfigurationModel) -> List[float]:
        user_preferences = preferences.getAllUserPreferences()
        feature_list = self.product_structure.get_list_of_features()
        user_scores = []
        for user_pref in user_preferences:
            feature_scores = []
            for feature in feature_list:
                char_list = feature.get_children_characteristics()
                in_to_rate_rating = 0
                avg = 0
                for char in char_list:
                    if char.elementId in toRate.configuration:
                        in_to_rate_rating = user_pref.getRatingByCode(char.elementId).getValue()
                    avg += user_pref.getRatingByCode(char.elementId).getValue()
                if len(char_list) > 0 :
                    avg = avg / len(char_list)
                map_function = MapToPercent(1,-1)
                feature_scores.append(map_function.applyToValue(in_to_rate_rating - avg))
            user_scores.append(self.featureListToValueFunction.convertToFloat(feature_scores))
        return user_scores