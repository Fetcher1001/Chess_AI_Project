from const import *
from square import Square
from piece import *
from neural_net import *
from move import Move
import numpy as np
class InputOutput():


    def __init__(self):
        self.board_input = [[0 for i in range(COLS)] for n in range(ROWS)]
        self.piece_list = ["pawn", "knight", "bishop", "rook", "queen", "king"]
        self.find_piece_move = lambda x: np.argmax(x) # find most likely piece or move



    def read_input(self, board): #
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    self.board_input[row][col] = board.squares[row][col].piece.value
                else:
                    self.board_input[row][col] = 0




    def ai_move(self, board):
        pass


    def ai_input_output(self, board):
        ai = chess_ai(board)
        piece_move = ai.neural_net()
        p = piece_move[0]
        m = piece_move[1]

        p_index = self.find_piece_move(p)
        piece = self.piece_list[p_index]


        move_index = self.find_piece_move(m)
        move_row = move_index // 8
        move_col = move_index % 8

        return [piece, move_row, move_col]


    def find_piece_position(self, piece_type, target_field, player_color):
        possible_positions = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == piece_type and self.color[row][col] == player_color:
                    legal_moves = self.board.calc_moves(row, col)
                    if target_field in legal_moves:
                        possible_positions.append((row, col))
        return possible_positions

