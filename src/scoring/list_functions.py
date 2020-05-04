from typing import List
from functools import reduce
import operator 

class ListFunction:
    pass
class ListToListFunction(ListFunction):
    def applyToList(self, list : List[float]) -> List[float]:
        pass
class ListToValueFunction(ListFunction):
    def convertToFloat(self, list : List[float]) -> float:
        pass

class Average(ListToValueFunction):
    def convertToFloat(self, list : List[float]) -> float:
        score = len(list)
        if score == 0:
            score = 1
        if list:
            return reduce(operator.add, list) / score
        else:
            return 0.0

class Min(ListToValueFunction):
    def convertToFloat(self, list : List[float]) -> float:
        return min(list)

class Product(ListToValueFunction):
    def convertToFloat(self, list : List[float]) -> float:
        return reduce(operator.mul, list)
