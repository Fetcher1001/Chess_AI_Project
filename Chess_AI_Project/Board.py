import copy

from const import *
from square import Square
from piece import *
from move import Move
from sound import Sound
import os

class Board:
    def __init__(self):
        self.squares= [[0 for row in range(ROWS)] for col in range(COLS)]

        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def is_checkmate(self, color):
        """
        Prüft, ob der Spieler der angegebenen Farbe im Schachmatt steht.
        :param color: Die Farbe des Spielers, dessen König geprüft wird ('white' oder 'black').
        :return: True, wenn der König im Schachmatt ist, sonst False.
        """
        # Finde die Position des Königs der angegebenen Farbe
        king_row, king_col = None, None
        for row in range(8):  # Annahme: ROWS = 8
            for col in range(8):  # Annahme: COLS = 8
                piece = self.squares[row][col].piece
                if isinstance(piece, King) and piece.color == color:
                    king_row, king_col = row, col
                    break
            if king_row is not None:
                break

        if king_row is None:
            return False  # König nicht gefunden (sollte nicht passieren)

        # Bestimme die Farbe des Gegners
        opponent_color = 'black' if color == 'white' else 'white'

        # Prüfe, ob der König im Schach steht
        in_check = False
        for row in range(8):
            for col in range(8):
                piece = self.squares[row][col].piece
                if piece and piece.color == opponent_color:
                    piece.clear_moves()  # Bereinige vorherige Züge
                    self.calc_moves(piece, row, col, bool=False)  # Berechne alle möglichen Züge ohne Schachprüfung
                    for move in piece.moves:
                        if move.final.row == king_row and move.final.col == king_col:
                            in_check = True
                            break
                if in_check:
                    break
            if in_check:
                break

        if not in_check:
            return False  # König nicht im Schach, also kein Schachmatt

        # Prüfe, ob der Spieler legale Züge hat
        has_legal_moves = False
        for row in range(8):
            for col in range(8):
                piece = self.squares[row][col].piece
                if piece and piece.color == color:
                    piece.clear_moves()  # Bereinige vorherige Züge
                    self.calc_moves(piece, row, col, bool=True)  # Berechne legale Züge (kein Schach erlaubt)
                    if piece.moves:  # Wenn das Stück mindestens einen legalen Zug hat
                        has_legal_moves = True
                        break
                if has_legal_moves:
                    break
            if has_legal_moves:
                break

        # Schachmatt, wenn der König im Schach ist und keine legalen Züge möglich sind
        return in_check and not has_legal_moves

    def move(self,piece, move, testing = False):
        initial = move.initial
        final = move.final
        en_passant_empty = self.squares[final.row][final.col].isempty()


        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        if isinstance(piece, Pawn):

            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                self.squares[initial.row][initial.col+ diff].piece = None
                self.squares[final.row][final.col].piece = piece
                if testing:
                    sound = Sound(
                        os.path.join(
                            'C:\\Users\johan\john_programms\Chess_AI_Project\\assets\sounds\capture.wav'))
                    sound.play()

            else:
               # pawn promotion
               self.check_promotion(piece, final)


        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])


        piece.is_moved = True
        print(f"{piece} bewegt: {piece.is_moved}")

        piece.clear_moves()

        self.last_move = move

    def valid_move(self, piece, move):
        if isinstance(piece, King) and abs(move.initial.col - move.final.col) == 2:
            return not piece.is_moved
        return move in piece.moves

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing= True)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_rival_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool= False)

                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True

        return False

        pass
    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def set_true_en_passant(self, piece):

        if not isinstance(piece, Pawn):
            return

        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_pessant = False

        piece.en_pessant = True


    def calc_moves(self, piece, row, col, bool = True):
        '''
            Calculate all the possible or valid moves of an specific piece on a specific position
        :param piece:
        :param row:
        :param col:
        :return:
        '''
        def pawn_moves():

            steps = 1 if piece.is_moved else 2

            start = row + piece.dir
            end = row +(piece.dir *(1+steps))

            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        initial = Square(row, col)
                        final = Square(possible_move_row,col)
                        move = Move(initial, final)
                        #check potentail check
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                    else: # blocked move
                        break
                else: # not in range
                    break

            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col +1]

            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):

                        initial = Square(row,col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)

                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

            #en pessand

            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
            #left en pessant
            if Square.in_range(col - 1) and row == r:
                if self.squares[row][col -1].has_rival_piece(piece.color):
                    p = self.squares[row][col -1].piece
                    if isinstance(p, Pawn):
                        if p.en_pessant:
                            initial = Square(row, col)
                            final = Square(fr, col-1, p)

                            move = Move(initial, final)
                            # check potentail check
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

            # right en passent
            if Square.in_range(col + 1) and row == r:
                if self.squares[row][col +1].has_rival_piece(piece.color):
                    p = self.squares[row][col +1].piece
                    if isinstance(p, Pawn):
                        if p.en_pessant:
                            initial = Square(row, col)
                            final = Square(fr, col + 1, p)

                            move = Move(initial, final)
                            # check potentail check
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)




        def knight_move():
            possible_moves = [(row-2, col+1),
                              (row-1, col+2),
                              (row+1, col+2),
                              (row+2, col+1),
                              (row+2, col -1),
                              (row+1, col-2),
                              (row-1, col-2),
                              (row-2, col-1)]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                   if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):

                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)

                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else:
                                break
                        else:
                            piece.add_move(move)




        def straightline_moves(incrs):
            for inc in incrs:
                row_incr, col_incr = inc
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):

                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)

                        move = Move(initial, final)

                        if self.squares[possible_move_row][possible_move_col].isempty():
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

                        elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

                            break #enemy piece

                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break  #team piece


                    else: #not in range
                        break
                    #incrementing
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                (row-1, col+0), #up
                (row-1, col +1), #up-right
                (row+0, col +1), #right
                (row+1, col+1), #down-right
                (row+1, col+ 0),# down
                (row+1, col-1), #down-left
                (row+0, col-1), #left
                (row-1, col-1) # up-left
            ]
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)

                        move = Move(initial, final)

                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else:
                                break
                        else:
                            piece.add_move(move)

            # castling moves
            if not piece.is_moved:

            #queen casteling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.is_moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece(): # casstling not possible bc pieces in between
                                break

                            if c == 3:
                                # adds left rook to king
                                piece.left_rook = left_rook
                                #rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial,final)


                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)
                                piece.add_move(moveK)

                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        left_rook.add_move(moveR)

                                        piece.add_move(moveK)
                                else:
                                    left_rook.add_move(moveR)
                                    piece.add_move(moveK)

            # king casteling mergeable
            right_rook = self.squares[row][7].piece
            if isinstance(right_rook, Rook):
                if not right_rook.is_moved:
                    for c in range(5, 7):
                        if self.squares[row][c].has_piece():  # casstling not possible bc pieces in between
                            break

                        if c == 6:
                            # adds right rook to king
                            piece.right_rook = right_rook
                            # rook move
                            initial = Square(row, 7)
                            final = Square(row, 5)
                            moveR = Move(initial, final)


                            # king move
                            initial = Square(row, col)
                            final = Square(row, 6)
                            moveK = Move(initial, final)

                            if bool:
                                if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                    right_rook.add_move(moveR)

                                    piece.add_move(moveK)
                            else:
                                right_rook.add_move(moveR)
                                piece.add_move(moveK)


        if isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, Knight):
            knight_move()
        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1,1),# up right
                (-1,-1),# up left
                (1,1), #down right
                (1,-1) #down left
            ])
        elif isinstance(piece, Rook):
            straightline_moves([
                (-1,0), #up
                (0,1), # right
                (1,0), # down
                (0,-1) # right
            ])
        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 1),  # up right
                (-1, -1),  # up left
                (1, 1),  # down right
                (1, -1), # down left
                (-1, 0),  # up
                (0, 1),  # left
                (1, 0),  # down
                (0, -1)  # right
            ])
        elif isinstance(piece, King):
            king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6,7) if color == 'white' else (1,0)

        # Pawn initialization
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # Knight initialization
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # Bishop initialization
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # Rook initialization
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # Queen initialization
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # King initialization
        self.squares[row_other][4] = Square(row_other, 4, King(color))


