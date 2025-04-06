import copy
from Input_output_AI import *
import numpy as np
from Board import *

class chess_ai():

    def __init__(self,board, board_input, color):
        self.input = np.array(board_input)
        self.input_neuron = np.flatten(self.input)

        self.board = board                                                      
        self.color = color
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

        hidden1_input = np.matmul(self.input_neuron, self.input_hidden1) + self.bias_hidden1
        hidden1_output = chess_ai.relu(hidden1_input)

        hidden2_input = np.matmul(self.hidden1_hidden2, hidden1_output) + self.hidden1_hidden2_bias
        hidden2_output = chess_ai.relu(hidden2_input)

        move_input = np.matmul(self.hidden2_output_move, hidden2_output) + self.hidden2_output_move_bias
        move_output = chess_ai.relu(move_input)

        piece_input = np.matmul(self.hidden2_output_piece, hidden2_output) + self.hidden2_output_piece_bias
        piece_output = chess_ai.relu(piece_input)

        return [piece_output, move_output]


    def backprob_neural_net(self):
        pass

        
    def loss(self, board, piece_type, move_row, move_col, player_color):
        board_copy = copy.deepcopy(board)
        io = InputOutput()


        possible_moves = io.find_piece_position(board, piece_type, (move_row, move_col), player_color)
        if not possible_moves:
            return 1000

        initial_row, initial_col = possible_moves[0]

        move = Move(Square(initial_row, initial_col), Square(move_row, move_col))

        piece = board.squares[initial_row][initial_col].piece

        if board.valid_move(piece, move):
            board_copy.move(piece, move)

            io.read_input(board_copy)
            update_input = io.board_input

            score = sum([val for row in update_input for val in row if val >0])

            if player_color == "white":
                loss = -score
            else:
                loss = score
        else:
            loss = 1000

        return loss

      def train_step(self):
          piece, moe_row, move_col = self.neural_net()
          loss_value = self.loss(self.board)



















