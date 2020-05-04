from model.configuration_model import ConfigurationModel, ConfigurationVariablesModel
import math
import pytest

class TestConfigurationModel:
    def test_simple_parsing(self):
        data = {
            'configuration': ['code1', 'code2'],
            'variables': [
                {
                    'code': 'abc',
                    'value': 1
                }
            ]
        }
        conf = ConfigurationModel(data)
        assert len(conf.configuration) == 2
        assert len(conf.variables) == 1

class TestConfigurationVariableModel:
    def test_simple_parsing(self):
        data = {
            'code': 'abc',
            'value': 1
        }
        var = ConfigurationVariablesModel(data)
        assert var.code == 'abc'
        assert var.value == 1