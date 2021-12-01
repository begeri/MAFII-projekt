import chess
import math
import random

#exploration constant
c=2
#simulations:
simCtr=0
#root node:
root=0

#Szótár ami a meglátogatott csúcsokat tartalmazza
nodes={}

class Node():
  def __init__(self, state):
    #milyen játékállás ez, chess-Boart típusó objektum
    self.state=state
    #gyerekek a fában (nodeok)
    self.children=[]
    #még nem nézett lépések
    self.not_visited=list(self.state.legal_moves)
    #szülő a fában
    self.parent=None
    #number of simulations
    self.N=0
    #number of wins
    self.w=0
    #number of parent simulation
    self.parN=0
    
    
    
# esetleg bevinni self.ucb-be??
def ucb(node):
  '''
  Return the UCB value of the given node
  '''
  result = node.w+c*math.sqrt((math.log(simCtr)+10**-6)/(node.N+10**-10))
  return result

def rollout(node):
  '''
  Plays out a random game, on the given node's board
  '''
  board=node.state.copy()
  global simCtr

  while(board.outcome()==None):
    legal_moves=list(board.legal_moves)
    board.push(random.choice(legal_moves))  
  simCtr+=1

  return board.outcome()

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
  
  child_state=node.state.copy()
  child_state.push(move)

  child=Node(child_state)
  #beállítani a szülűnek ezt
  child.parent=node
  #a not_visitedet legalmoveokkal inicializálni (default, elv nem kell)

  #a parent.children-t updatelni, belerakni a child-ot
  node.children.append(child)

  return child

def rollback():
  pass
