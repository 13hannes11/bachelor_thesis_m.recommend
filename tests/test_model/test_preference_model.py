from model.preferences_model import Preferences, Rating, UserPreference
import math
import pytest

class TestRating:
    def test_range_conversion_minus_one_to_zero(self):
        data = {
            'code': 'abs',
            'value': 0
        }
        assert math.isclose(0, Rating(data).getValue())
    def test_range_conversion_one_to_one(self):
        data = {
            'code': 'abs',
            'value': 1
        }
        assert math.isclose(1, Rating(data).getValue())
    def test_range_conversion_zero_to_half(self):
        data = {
            'code': 'abs',
            'value': 0.5
        }
        assert math.isclose(0.5, Rating(data).getValue())
    def test_value_to_large(self):
        with pytest.raises(ValueError):
            data = {
                'code': 'abs',
                'value': 1.1
            }
            rating = Rating(data)
    def test_value_to_small(self):
        with pytest.raises(ValueError):
            data = {
                'code': 'abs',
                'value': -0.1
            }
            rating = Rating(data)

class TestUserPreference:
    data = {
        'user': "user0",
        'ratings':[ {
                'code': 'abs',
                'value': 0
            }, {
                'code': '2',
                'value': 1
            }, {
                'code': '3',
                'value': 0.5
            }
        ]
    }
    def test_get_all_ratings(self):
        user_pref = UserPreference(self.data)
        assert len(user_pref.getAllRatings()) == 3
    def test_get_rating_by_code(self):
        user_pref = UserPreference(self.data)
        rating = user_pref.getRatingByCode('2')
        assert rating.code == '2'
        assert rating.getValue() == 1
    def test_get_rating_by_code_default(self):
        user_pref = UserPreference(self.data)
        rating = user_pref.getRatingByCode('notFOUND')
        assert rating.code == 'notFOUND'
        assert rating.getValue() == 0.5

class TestPreferences:
    preferences = Preferences({
        'preferences': [
            {
                'user': "user0",
                'ratings':[ {
                        'code': 'in_both',
                        'value': 0
                    }, {
                        'code': 'only_in_one',
                        'value': 1
                    }, {
                        'code': '3',
                        'value': 0.5
                    }
                ]
            },
            {
                'user': "user1",
                'ratings':[ {
                        'code': 'in_both',
                        'value': 1
                    }, {
                        'code': '3',
                        'value': 1
                    }
                ]
            }
        ]
    })
    def test_get_all_user_preferences(self):
        assert len(self.preferences.getAllUserPreferences()) == 2
    def test_get_all_rating_by_code(self):
        assert len(self.preferences.getAllRatingsByCode('only_in_one')) == 2
        assert len(self.preferences.getAllRatingsByCode('in_both')) == 2
    def test_get_all_users(self):
        assert len(self.preferences.getAllUsers()) == 2
        assert "user0" in self.preferences.getAllUsers()
        assert "user1" in self.preferences.getAllUsers()
    def test_get_rating_by_user_and_code(self):
        assert self.preferences.getRatingValueByUserAndCode("user0", "only_in_one") == 1
    def test_empty_preferences(self):
        assert len(Preferences({ 'preferences' : []}).getAllUsers()) == 0
    def test_getIndividual_preferences(self):
        assert len(self.preferences.getIndividualPreferences()) == 2
    
