import math
import Utils

class NeuralNode(object):
    def __init__(self):
        #temp actual value
        self.value = 0

        #bias is for node
        self.bias = 0

        #weights are for links
        self.weights = []

    def CalculateValue(self, _input, _bias):
        self.value = Utils.Sigmoid(_input + _bias)