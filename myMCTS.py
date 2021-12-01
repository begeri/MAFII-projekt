import chess
import math
import random
import datetime

#exploration constant
c=2
#VIRTUAL BOARD
vboard = chess.Board()
#Melyik játékosként játszunk?
play_as=None

class Node():
  def __init__(self, state):
    #milyen játékállás ez, chess-Board típusó objektum
    self.state=state
    #gyerekek a fában (nodeok)
    self.children=[]
    #még nem nézett lépések
    vboard.set_fen(state)
    self.not_visited=list(vboard.legal_moves)
    #szülő a fában
    self.parent=None
    #number of simulations
    self.N=0
    #number of wins
    self.w=0
    #a lépés, amivel ideérkeztünk
    self.action = ''
  
  def __str__(self):
    return 'state: ' + str(self.state) + '\nchildren: ' + str(len(self.children)) + '\nnem látott lépések = '+ str(len(self.not_visited)) + '\nrolloutok száma = ' + str(self.N) + '\ngyőztes rolloutok száma ' + str(self.w) + '\nself.action= ' + str(self.action)
    
def ucb(node):
  '''
  Returns the UCB value of the given node
  '''
  result = node.w+c*math.sqrt((math.log(node.parent.N)+10**-6)/(node.N+10**-10))
  return result

def rollout(node):
  '''
  Plays out a random game, on the given node's board
  '''
  vboard.set_fen(node.state)

  while(vboard.outcome()==None):
    legal_moves=list(vboard.legal_moves)
    vboard.push(random.choice(legal_moves))
  
  if vboard.result()=='1/2-1/2':
    return 0.5
  winner = (vboard.result()=='1-0')
  if winner==play_as:
    return 1
  return 0
  
def selection(node):
  
  '''
  Kezdetben vagyunk a gyökérben. Ált esetben egy csúcsban vagyunk.  
  Ha van olyan gyereke az adott csúcsnak, amit még nem vizsgáltunk, visszaadjuk ezt a csúcsot.
  Ha nincs ilyen gyereke a vizsgált csúcsnak, vasszük a gyerekek közül a maxUCB értékűt. És erre a selection() 
  '''
  if node.not_visited:
    return node
  #A gyerekekből a max UCB értékűt kiválasztani
  maxUCB_child=max(node.children, key=lambda i: ucb(i))
  #és meghívni rá a selection-t
  return selection(maxUCB_child)

def expansion(node):
  #move-ot kiválasztani, és törölni a moveot a parent.not_visited listából
  move=random.choice(node.not_visited)
  node.not_visited.remove(move)
  #ebből egy csúcsot csinálni, hozzáadni a fához
  vboard.set_fen(node.state)
  vboard.push(move)
  child=Node(vboard.fen())
  #beállítani a szülőnek ezt
  child.parent=node
  #megjegyezni, hogy érkeztünk ide
  child.action=move
  #a parent.children-t updatelni, belerakni a child-ot
  node.children.append(child)
  return child

def rollback(node, result):
  node.w += result
  node.N += 1
  if node.parent!=None:
    rollback(node.parent, result)

def make_move(board, time_limit):
  root=Node(board.fen())
  play_as = chess.WHITE
  #amíg van idő, addig selection, expansion, rollout, rollback, repeat
  begin = datetime.datetime.utcnow()
  while datetime.datetime.utcnow() - begin < datetime.timedelta(seconds=time_limit):
    new_child=expansion(selection(root))
    rollback(new_child, rollout(new_child))
  print('\n#simulations = ', root.N)
  best_child = max(root.children, key=lambda i: i.w/i.N)
  return best_child.action