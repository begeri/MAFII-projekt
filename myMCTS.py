
import chess
import math
import random
import datetime

#exploration constant
c=2

#root node:
root=0
#VIRTUAL BOARD
board = chess.Board()

#Szótár ami a meglátogatott csúcsokat tartalmazza
nodes={}

#Melyik játékosként játszunk?
#lehet vilgásonak True és sötétnek False
play_as=True


class Node():
  def __init__(self, state):
    #milyen játékállás ez, chess-Board típusó objektum
    self.state=state
    #gyerekek a fában (nodeok)
    self.children=[]
    #még nem nézett lépések
    board.set_fen(state)
    self.not_visited=list(board.legal_moves)
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
    
    
    
# esetleg bevinni self.ucb-be??
def ucb(node):
  '''
  Return the UCB value of the given node
  '''
  result = node.w+c*math.sqrt((math.log(node.parent.N)+10**-6)/(node.N+10**-10))
  return result

def rollout(node):
  '''
  Plays out a random game, on the given node's board
  '''
  board.set_fen(node.state)

  while(board.outcome()==None):
    legal_moves=list(board.legal_moves)
    board.push(random.choice(legal_moves)) 

  
  if board.result()=='1/2-1/2':
    return 0.5

  winner = (board.result()=='1-0')

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
      #Erre kell majd meghívni az expansiont
      # Selection proceeds until you reach a position where not all of the child positions have statistics recorded.
  
  else:
    #A gyerekekből a max UCB értékűt kiválasztani
    maxUCB_child=max(node.children, key=lambda i: ucb(i))
    #és meghívni rá a selection-t
    selection(maxUCB_child)

def expansion(node):
  #move-ot kiválasztani, és törölni a moveot a parent.not_visited listából
  move=random.choice(node.not_visited)
  node.not_visited.remove(move)
  #ebből egy csúcsot csinálni, hozzáadni a fához
  board.set_fen(node.state)
  board.push(move)
  child=Node(board.fen())
  #beállítani a szülűnek ezt
  child.parent=node
  #megjegyezni, hogy érkeztünk ide
  child.action=move
    #a parent.children-t updatelni, belerakni a child-ot
  node.children.append(child)
  return child

def rollback(node, result):
  # outcome = 0, 0.5, 1
  #input: egy csúcs, amiből volt a rollout, és egy eredmény a rolloutból. 
  #lépegetek vissza mindig a szülőre a csúcsból, közben:
  
  node.w += result
  node.N += 1
  
  if node.parent!=None:
    rollback(node.parent, result)

def make_move(board, time_limit):
  root=Node(board.fen())

  
  #amíg van idő, addig selection, expansion, rollout, rollback, repeat
  begin = datetime.datetime.utcnow()
  while datetime.datetime.utcnow() - begin < datetime.timedelta(seconds=time_limit):
    new_child=expansion(selection(root))
    rollback(new_child, rollout(new_child))
    #debugging part:
    print(root)
    if len(root.not_visited) < 1:
      print(root.children[0])
  
  best_child = max(root.children, key=lambda i: i.w/i.N)
  return best_child.action