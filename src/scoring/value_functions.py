import math

class ValueToValueFunction:
    def applyToValue(self, value : float) -> float :
        return value

class MapToPercent(ValueToValueFunction):
    def __init__(self, max_val : float, min_val : float):
        self.max_val = max_val
        self.min_val = min_val
    def applyToValue(self, value : float) -> float :
        return (value - self.min_val) / abs(self.min_val - self.max_val)

class HighpassFilterFunction(ValueToValueFunction):
    def __init__(self,  cutoff : float, floor_value=0):
        self.cutoff = cutoff
        self.floor_value = floor_value
    def applyToValue(self, value : float) -> float :
        if value < self.cutoff:
            return self.floor_value
        else: 
            return value

class LowpassFilterFunction(ValueToValueFunction):
    def __init__(self,  cutoff : float, ceiling_value=1):
        self.cutoff = cutoff
        self.ceiling_value = ceiling_value
    def applyToValue(self, value : float) -> float :
        if value > self.cutoff:
            return self.ceiling_value
        else: 
            return value

class PowerFunction(ValueToValueFunction):
    def __init__(self,  power : float):
        self.power = power 

    def applyToValue(self, value : float) -> float :
        return math.pow(value, self.power)