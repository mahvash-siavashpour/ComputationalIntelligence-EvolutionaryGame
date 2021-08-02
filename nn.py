import numpy as np


class NeuralNetwork():

    def __init__(self, layer_sizes):
        # TODO
        # layer_sizes example: [4, 10, 2]
        self.w1 = np.random.normal(0, 1, size=(layer_sizes[1], layer_sizes[0]))
        self.b1 = np.random.normal(0, 1, size=(layer_sizes[1], 1))
        self.w2 = np.random.normal(0, 1, size=(layer_sizes[2], layer_sizes[1]))
        self.b2 = np.random.normal(0, 1, size=(layer_sizes[2], 1))
        self.sizes = layer_sizes


    def activation(self, x):
        return 1 / (1 + np.exp(-x))
        # TODO

    def forward(self, x):
        # print(self.w1, self.b1)
        input_layer = np.reshape(x, (self.sizes[0], 1))
        hidden_layer = self.activation(np.dot(self.w1, input_layer) + self.b1)
        output_layer = self.activation(np.dot(self.w2, hidden_layer) + self.b2)
        # file = open("log.txt", 'w')
        # file.write(output_layer)
        return output_layer
        # TODO
        # x example: np.array([[0.1], [0.2], [0.3]])
