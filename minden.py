import chess
import random

board = chess.Board()

# outcome

outcome = board.outcome()
if outcome:
    if outcome.winner == chess.WHITE:
        print("white won")
    elif outcome.winner == chess.BLACK:
        print("black won")
    else:
        print("draw")
else:
    print("game not yet over")

#sok szimuláció
'''
whiteWin=0
blackWin=0
for i in range(1):
  board = chess.Board()
  simulation()
  if board.outcome().winner == chess.WHITE:
    whiteWin=whiteWin+1
  elif board.outcome().winner == chess.BLACK:
    blackWin=blackWin+1
  else:
    pass

print('white', whiteWin)
print('black', blackWin)
'''