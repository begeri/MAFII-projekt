import chess
import random

#Függvények
#simulation
def simulation(board):
  '''
  Plays out a random game, on the given board
  '''
  while(board.outcome()==None):
    legal_moves=list(board.legal_moves)
    board.push(random.choice(legal_moves))


def play_n_moves(board, n):
  '''
  Plays n moves on the given board
  '''
  for i in range(n):
    legal_moves=list(board.legal_moves)
    board.push(random.choice(legal_moves))

def make_move(board, move):
  '''
  Plays the given move on the given board. Complains, if the move is not legal.
  The move should be given as a string.
  '''


  pass
  
#Teszttér

board=chess.Board()

board_curr=board.copy()



print(board)
print(board.legal_moves)

move = chess.Move.from_uci("e2e4")
board.push(move)
print(board)




