import chess
import random
import pandas as pd

board = chess.Board()

'''
  current_player : chess.WHITE == True / False

  game_state : board

  next_state : board.push(Nf3)

  legal_plays: board.legal_moves

  winner: board.outcome.winner == chess.WHITE
'''

#print(chess.BLACK)
legal_moves=list(board.legal_moves)
#print(legal_moves)
#board.push(random.choice(legal_moves))
#print(board.outcome())


#simulation
def simulation():
  while(board.outcome()==None):
    legal_moves=list(board.legal_moves)
    board.push(random.choice(legal_moves))

data = pd.read_csv('chess.csv')
data = data.drop(data[data['victory_status']=='outoftime'].index)


plays = {} # keys: (player, state)
wins = {}
board = chess.Board()
winner=list(data['winner'])
moves=list(data['moves'])

for i in range(len(data)):
  board.reset()
  states = []
  m = moves[i].split()
  for j in range(len(m)):
    # update
    board.push_san(m[j])


  

#chess[3:4]['moves']

print(moves[1].split())