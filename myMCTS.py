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
  '''
  Csúcsosztály, amikkel lehet fát építeni. Tartalmazza a játékállást FEN kódolásban és a kód futása során használt jellemzőit az állásnak
  '''
  def __init__(self, state):
    #milyen játékállás ez, fen stringként
    self.state=state
    #gyerekek a fában (nodeok)
    self.children=[]
    #még nem nézett lépések
    vboard.set_fen(state)
    self.not_visited=list(vboard.legal_moves)   
    #szülő a fában
    self.parent=None
    #a leszármazottaiból lefuttatott kiértékelések száma
    self.N=0
    ##a leszármazottak kiértékeléseinek összértéke
    self.w=0
    #a lépés, amivel ideérkeztünk
    self.action = ''
    #ezen állásban vége van-e a játéknak
    self.outcome = None
  
  def __str__(self):
    return 'state: ' + str(self.state) + '\nchildren: ' + str(len(self.children)) + '\nnem látott lépések = '+ str(len(self.not_visited)) + '\nrolloutok száma = ' + str(self.N) + '\ngyőztes rolloutok száma ' + str(self.w) + '\nself.action= ' + str(self.action)
    
def ucb(node):
  '''
  Returns the UCB value of the given node
  '''
  result = node.w+c*math.sqrt((math.log(node.parent.N)+10**-6)/(node.N+10**-10))
  return result


def pieces(fen):
  '''
  Egy fen kódolású állásból kigyűjti, az egyes figuratípusokból hány darab van a pályán.
  '''
  pieces = {}
  for char in 'KkQqRrNnBbPp':
    pieces[char] = 0
  for i in fen.split()[0]:
    if i in pieces:
      pieces[i]+=1
  return pieces
  
def eval(node):
  '''
  Világosként megnézzük, hogy nyertünk-e, ha nem összeadjuk a pályán lévő figurák értékét. Így értékeljük az állást.
  '''
  #A győzelem értéke:
  winWt=10
  #Ha vége a játéknak, adjuk vissza a győzelem hírét a győzelem súlyával!
  if node.outcome != None:
    return node.outcome*winWt
  p=pieces(node.state)
  kingWt=200
  queenWt=9
  rookWt=5
  knightWt=3
  bishopWt=3
  pawnWt=1
  # score max = 39 egyik készletre nézve
  score=queenWt*(p['Q']-p['q']) + rookWt*(p['R']-p['r']) + knightWt*(p['N']-p['n']) + bishopWt*(p['B']-p['b']) + pawnWt*(p['P']-p['p'])
  #return score/30
  return math.tanh(score)/(score+1.01)
  
def selection(node):
  
  '''
  Kezdetben vagyunk a gyökérben. Ált esetben egy csúcsban vagyunk.  
  Ha van olyan gyereke az adott csúcsnak, amit még nem vizsgáltunk, visszaadjuk ezt a csúcsot.
  Ha nincs ilyen gyereke a vizsgált csúcsnak, vasszük a gyerekek közül a maxUCB értékűt. És erre a selection() 
  '''
  #Ha van a csúcsnak mg nem vizsgált lépése
  if node.not_visited:
    return node
  #A gyerekekből a max UCB értékűt kiválasztani
  if node.outcome==None:
    maxUCB_child=max(node.children, key=lambda i: ucb(i))
    #és meghívni rá a selection-t
    return selection(maxUCB_child)
  #Ha vége van a játéknak, nem tudunk innen tovább lépni.
  return node

def expansion(node):
  '''
  Egy adott levélnek egy lehetséges lépését hozzá akarjuk adni a fához. Létrehozunk egy 'child' csúcsot az input még meg nem nézett lépéseiből az egyiket meglépve.
  Ennek a megfelelő adattagjait beállítjuk, illetve a szülő még nem látott gyerekeiből kitöröljük és hozzáadjuk a már látott gyerekekhez.
  '''
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
  #vége van e
  if vboard.outcome()!=None:
    # FEHÉR NYER
    if chess.Board.outcome(vboard).winner:
      child.outcome = 1
    # FEKETE NYER
    elif not chess.Board.outcome(vboard).winner:
      child.outcome = -1
    #DÖNTETLEN
    else:
      child.outcome = 0.5

  #a parent.children-t updatelni, belerakni a child-ot
  node.children.append(child)
  return child

def rollback(node, result):
  '''
  Egy új kiértékeléssel frissítjük a fában az input csúcsot és az őseit.
  '''
  node.w +=result
  node.N +=1
  if node.parent!=None:
    rollback(node.parent, result)

def make_move(board, time_limit):
  '''
  board - játékállás, chess.Board típusú objektum
  time_limit - gondolkodási idő másodpercben
  Megkap egy játékállást, eldönti milyen játékos lép innen, majd minden értékelést eszerint végezve a kapott gondolkodási idő hosszáig építi a keresőfát,
  finomítja a csúcsok értékelését.
  Majd visszaadja a fában az állás legígéretesebbnek tűnő gyerekének a lépését. 
  '''
  #Gyökér inicializálása
  root=Node(board.fen())
  #Milyen játékosként játszunk
  player = board.fen().split()[1]
  if player == 'w':
    play_as=1
  else:
    #Mivel az értékelőfüggvény a fehér szempontjából nézi az ábrát -1-szeresét kell venni az értéknek
    play_as=-1
  #print(play_as) - for testing sake
  
  #amíg van idő, addig selection, expansion, eval, rollback, repeat
  begin = datetime.datetime.utcnow()
  while datetime.datetime.utcnow() - begin < datetime.timedelta(seconds=time_limit):
    #A selection megad egy olyan leszármazottat, aminek van még nem vizsgált lépése
    child=selection(root)
    #Ha nincs vége a játéknak
    if child.outcome==None:
      #Létrehoz egy eddig nem vizsgált játékállást
      new_child = expansion(child)
    #Ha vége van a játéknak
    else:
      new_child=child
      pass
    #Frissíti az új gyerek őseinek az értékelését az új gyerek értékétől függően
    rollback(new_child, play_as*eval(new_child))
    
  print('#simulations = ', root.N)# - testing stuff
  best_child = max(root.children, key=lambda i: i.w/i.N)
  print('best_eval', play_as*eval(best_child))# - testing stuff
  return best_child.action
