from scoring.list_functions import Average, Product
import math

class TestListToValueFunctionAverage:
    def test_simple_average(self):
        function = Average()
        list = [0.0, 1.0]
        assert math.isclose(0.5, function.convertToFloat(list))

class TestListToValueFunctionProduct:
    def test_simple_product(self):
        function = Product()
        list = [0.5, 0.5]
        assert math.isclose(0.25, function.convertToFloat(list))