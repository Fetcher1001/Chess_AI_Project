from const import *
from square import Square
from piece import *
from neural_net import *
from move import Move

class InputOutput():

    def __init__(self):
        self.board_input = [[0 for i in range(COLS)] for n in range(ROWS)]


    def read_input(self, board): #
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    self.board_input[row][col] = board.squares[row][col].piece.value
                else:
                    self.board_input[row][col] = 0




    def ai_move(self, board):
        ai_instance = chess_ai(board)
