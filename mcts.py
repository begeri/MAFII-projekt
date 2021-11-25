class MonteCarlo:

  def __init__(self, board, **kwargs):
    
    self.board = board
    self.states = []
    self.wins = {}
    self.plays = {}

  def update(self, state):
    self.states.append()

  def get_play(self):
      # Causes the AI to calculate the best move from the
      # current game state and return it.
      pass

  def tree_search(self):
    visited_states = set()
    states_copy = self.states[:]
    

  def selection(self):
    #állás->legalmoves->új állás (másolat)->legalmoves->repeat
    
    
    pass

  def expansion(self):
    pass

  def simulation(self):
    pass
  
  def backpropagation(self):
    pass