import numpy
import numpy as np


class chess_ai():

    def __init__(self,board):
        self.input = np.array(board)
        self.input_neuron = np.flatten(self.input)

        # weights and bias init ________________________________________________________________________________
        self.num_hidden1 = 128
        self.num_hidden2 = 64


        self.input_hidden1 = np.random.rand(self.num_hidden1, len(self.input_neuron))
        self.bias_hidden1 = np.random.rand(self.num_hidden1)

        self.hidden1_hidden2 = np.random.rand(self.num_hidden2, self.num_hidden1)
        self.hidden1_hidden2_bias = np.random.rand(self.num_hidden2)

        self.hidden2_output_move = np.random.rand(64, self.num_hidden2)# 64 zug
        self.hidden2_output_move_bias = np.random.rand(64)

        self.hidden2_output_piece = np.random.rand(6, self.num_hidden2)#6 figur
        self.hidden2_output_piece_bias = np.random.rand(6)

         #_____________________________________________________________________________________________________

        self.output = []
        self.depth = 3
        self.move_history = []


    @staticmethod
    def relu(x):
        return np.maximum(0,x)

    def neural_net(self):
        pass

        





