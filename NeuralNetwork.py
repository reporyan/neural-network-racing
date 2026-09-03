import math
from NeuralNode import NeuralNode
import random

class NeuralNetwork(object):
    def __init__(self, _load = "", _nn = None):
        #create the network nodes
        if(_load == ""):
            if(_nn is None):
                self.GenerateNeuralNetwork([20, 4])
                self.TotalRandomise()
            else:
                layers = []
                for layer in _nn.layers:
                    layers.append(len(layer))
                self.GenerateNeuralNetwork(layers)
        else:
            self.LoadFromFile(_load)

    def GenerateNeuralNetwork(self, _layers):
        #self.layersCounts = []
        #for layer in _layers:
            #self.layersCounts.append(len(layer))

        self.layers = []

        for i in _layers:
            self.layers.append([NeuralNode() for j in range(i)])
        
        #reference the nodes to eachother
        for i in range(len(self.layers) - 1):
            #link if there is a layer in front
            for startNode in self.layers[i]:
                for endNode in self.layers[i + 1]:
                    startNode.weights.append(0)

    def Process(self, _sensing):
        #for the first layer, the values are the inputs
        for i in range(len(self.layers[0])):
            self.layers[0][i].value = _sensing[i]

        #for each layer that takes input from another layer
        for i in range(1, len(self.layers)):
            #for every node in this current layer
            for j in range(len(self.layers[i])):
                node = self.layers[i][j]
                #set the total dot to 0
                totalInput = 0
                #add up the dot for every previous node
                for k in range(len(self.layers[i - 1])):
                    previousNode = self.layers[i - 1][k]
                    totalInput += (previousNode.value * previousNode.weights[j])
                #calc node and set as value
                node.CalculateValue(totalInput, node.bias)
        
        #return output (input) nodes
        networkOutput = []
        for node in self.layers[len(self.layers) - 1]:
            networkOutput.append(node.value)
        return networkOutput

    def DeepCopy(self):
        #constructor already does some work
        copy = NeuralNetwork("", self)
        for i in range(len(self.layers)):
            layer = self.layers[i]
            for j in range(len(layer)):
                node = layer[j]
                copyNode = copy.layers[i][j]
                copyNode.bias = node.bias
                for k in range(len(node.weights)):
                    copyNode.weights[k] = node.weights[k]

        #return
        return copy

    def TotalRandomise(self):
        for i in range(len(self.layers)):
            for j in range(len(self.layers[i])):
                self.layers[i][j].bias = random.uniform(-1, 1)
                for k in range(len(self.layers[i][j].weights)):
                    self.layers[i][j].weights[k] = random.uniform(-1, 1)

    def ChangeRandomise(self, _biasVarience, _weightVarience):
        for i in range(len(self.layers)):
            for j in range(len(self.layers[i])):
                self.layers[i][j].bias += random.gauss(0, _biasVarience)
                for k in range(len(self.layers[i][j].weights)):
                    self.layers[i][j].weights[k] += random.gauss(0, _weightVarience)

    def SaveToFile(self, fileName):
        with open(fileName, "w") as file:
            file.write(f"#{fileName}\n")

            #how many layers
            file.write(str(len(self.layers)) + '\n')

            #nodes in layer
            for layer in self.layers:
                #how many nodes in this layer
                file.write(str(len(layer)) + '\n')

            #nodes in layer
            for layer in self.layers:
                for node in layer:
                    #this nodes bias
                    file.write(str(node.bias) + '\n')

                    #for links
                    for weight in node.weights:
                        #this weight
                        file.write(str(weight) + '\n')

    def LoadFromFile(self, fileName):
        print(f"Loading{fileName}")
        with open(fileName, "r") as file:
            lines = file.readlines()
            i = 1

            #load layernum
            layerNum = int(lines[i])
            self.layers = []
            layers = []#layer counts
            i += 1

            #load node num for each layer
            for j in range(layerNum):
                layers.append(int(lines[i]))
                i += 1

            #generate
            self.GenerateNeuralNetwork(layers)

            #for each layer
            for layer in self.layers:
                #for each node
                for node in layer:
                    #set bias
                    node.bias = float(lines[i])
                    i += 1
                    #for each weight
                    for j in range(len(node.weights)):
                        node.weights[j] = float(lines[i])
                        i += 1

            #counts
            self.layersCounts = layers
            print(self.layersCounts)
