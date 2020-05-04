from typing import List

class Rating:
    def __init__(self, data):
        self.code = data['code']
        self.value = float(data['value'])
        if self.value < 0 or self.value > 1:
            raise ValueError("Value of rating has to be in interval [0,1]")
    def getValue(self):
        """ Returns rating value """
        return self.value

class UserPreference:
    def __init__(self, data):
        self.ratings : List[Rating] = []
        self.user : str = data['user']
        for rat in data['ratings']:
            self.ratings.append(Rating(rat))    
    def getAllRatings(self) -> List[Rating]:
        return self.ratings
    def getRatingByCode(self, code : str) -> Rating:
        return next(filter(lambda x : x.code == code, self.ratings), Rating({'code': code, 'value': 0.5 }))
    
class Preferences:
    def __init__(self, data={ 'preferences' : [] }):
        self.preferences : List[UserPreference] = [] 
        for pref in data['preferences']:
            self.preferences.append(UserPreference(pref))
    def getAllUserPreferences(self) -> List[UserPreference]:
        return self.preferences
    def getAllRatingsByCode(self, code) -> List[Rating]:
        list = []
        for user_pref in self.preferences:
            list.append(user_pref.getRatingByCode('code'))
        return list
        
    def getAllUsers(self) -> List[str] :
        list = []
        for userPref in self.preferences:
            if userPref.user not in list :
                list.append(userPref.user)
        return list
    def getRatingValueByUserAndCode(self, user, code) -> float:
        for userPref in self.preferences:
            if userPref.user == user :
                for rating in userPref.ratings:
                    if rating.code == code:
                        return rating.getValue()
        return 0.5

    def getIndividualPreferences(self):
        return list(map(lambda x: _create_preferences_and_add_user_pref(x), self.preferences))

def _create_preferences_and_add_user_pref(userPref):
    tmp = Preferences()
    tmp.preferences.append(userPref)
    return tmp