from typing import List

class ConfigurationVariablesModel:
    def __init__(self, data):
        self.value : str = data['value']
        self.code : str = data['code']

class ConfigurationModel:
    def __init__(self, data):
        self.configuration : List[str] = []
        self.variables : List[ConfigurationVariablesModel] = []
        if data is not None:
            self.configuration = data['configuration']
            if 'variables' in  data:
                for v in data['variables']:
                    self.variables.append(ConfigurationVariablesModel(v))
    