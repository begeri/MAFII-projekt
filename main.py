import chess
import random
import myMCTS as my

board=chess.Board()
test_node=my.Node(board.fen())

my.make_move(board, 3)