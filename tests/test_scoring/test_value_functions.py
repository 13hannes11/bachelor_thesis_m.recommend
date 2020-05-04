from scoring.value_functions import MapToPercent, ValueToValueFunction, HighpassFilterFunction, LowpassFilterFunction, PowerFunction
import math

class TestMapToPercent:
    def test_range_conversion(self):
        function = MapToPercent(-20, -40)
        assert math.isclose(1, function.applyToValue(-20))
        assert math.isclose(0, function.applyToValue(-40))
        assert math.isclose(0.5, function.applyToValue(-30))

class TestValueToValueFunction:
    def test_same_value(self):
        function = ValueToValueFunction()
        assert math.isclose(10, function.applyToValue(10))

class TestHighpassFilterFunction:
    def test_higher_value(self):
        function = HighpassFilterFunction(0.5)
        assert math.isclose(0.8, function.applyToValue(0.8))
    def test_lower_value(self):
        function = HighpassFilterFunction(0.5)
        assert math.isclose(0, function.applyToValue(0.3))
    def test_same_value(self):
        function = HighpassFilterFunction(0.5)
        assert math.isclose(0.5, function.applyToValue(0.5))

class TestLowpassFilterFunction:
    def test_higher_value(self):
        function = LowpassFilterFunction(0.5)
        assert math.isclose(1, function.applyToValue(0.8))
    def test_lower_value(self):
        function = LowpassFilterFunction(0.5)
        assert math.isclose(0.3, function.applyToValue(0.3))
    def test_same_value(self):
        function = LowpassFilterFunction(0.5)
        assert math.isclose(0.5, function.applyToValue(0.5))

class TestPowerFunction:
    def test_power_one(self):
        function = PowerFunction(10)
        assert math.isclose(1, function.applyToValue(1))
    def test_power_small_number(self):
        function = PowerFunction(4)
        assert math.isclose(0.0001, function.applyToValue(0.1))