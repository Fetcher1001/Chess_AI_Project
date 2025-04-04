from const import *
import os
class Piece:
    def __init__(self, name, color, value, texture = None, texture_rect = None):
        self.name = name
        self.color = color

        value_sing = 1 if color == 'white' else -1
        self.value = value * value_sing

        self.moves = []
        self.is_moved = False

        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def clear_moves(self):
        self.moves = []
    def set_texture(self,size = 80):
        self.texture = os.path.join(
            f'assets\images\imgs-{size}px/{self.color}_{self.name}.png'
        )

    def add_move(self, move):
        self.moves.append(move)

class Pawn(Piece):

    def __init__(self,color):
        self.dir = -1 if color == 'white' else 1
        self.en_pessant = False
        super().__init__('pawn', color, PAWN)

class Knight(Piece):
    def __init__(self,color):
        super().__init__('knight', color, KNIGHT)

class Bishop(Piece):
    def __init__(self,color):
        super().__init__('bishop', color, BISHOP)


class Rook(Piece):
    def __init__(self,color):
        super().__init__('rook', color, ROOK)

class Queen(Piece):
    def __init__(self,color):
        super().__init__('queen', color, QUEEN)

class King(Piece):
    def __init__(self,color):
        self.left_rook = None
        self.right_rook = None
        super().__init__('king', color, KING)

