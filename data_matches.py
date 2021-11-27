data = pd.read_csv('chess.csv')
data = data.drop(data[data['victory_status']=='outoftime'].index)
data = data.drop(data[data['victory_status']=='resign'].index)

# states = []
plays = {} # keys: (player, state)
wins = {}
board = chess.Board()
winner=list(data['winner'])
moves=list(data['moves'])

def current_player(i):
    if i%2 == 0:
        return 'white'
    if i%2 == 1:
        return 'black'

def update(state, i, j):
    wins[state] += i
    plays[state] += j

for i in range(len(data)):
    board.reset()
    m = moves[i].split()
    for j in range(len(m)):
        board.push_san(m[j])
        state = chess.Board.fen(board) #string representation
        # update
        if state not in plays.keys():
            plays[state] = 0
            wins[state] = 0
        if current_player(j) == winner[i]:
            update(state, 1, 1)
        if winner[i] == 'draw':
            update(state, 0.5, 1)
        else:
            update(state, 0, 1)
