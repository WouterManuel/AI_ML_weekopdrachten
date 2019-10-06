import itertools
import random

# posities op het bord, volgens coordinaten in een 2D lijst
board = {0: '', 1: '', 2: '', 3: '',
         4: '', 5: '', 6: '', 7: ''}

# dict met alle aangrenzende posities per positie op het bord
neighbours = {0: [3], 1: [2], 2: [1, 3, 4], 3: [0, 2, 5], 
              4: [2, 5], 5: [3, 4, 6, 7], 6: [5], 7: [5]}

# alle mogelijke te spelen kaarten
cards = ['A', 'A', 'H', 'H', 'V', 'V', 'B', 'B']

# elke A grenst aan een H
# elke H grenst aan een D
# elke D grenst aan een B
# elke A grenst NIET aan een D
# twee kaarten van dezelfde soort mogen niet buren zijn

# for loop
def is_valid(k_board):
    # for position on board
    for position in k_board.keys():
        # if position isnt empty, validate neighbours
        card_value = k_board[position]
        # if string is not empty
        if not not card_value:
            # list_neighbours= [x for x in neighbours[key]]
            neighbour_values = [k_board[v] for v in neighbours[position]]

            if card_value in neighbour_values: 
                return False
            elif (card_value == 'A' and 'H' not in neighbour_values): # or (card_value == 'H' and 'A' not in neighbour_values):
                 return False
            elif card_value == 'H' and 'V' not in neighbour_values:  # or (card_value == 'V' and 'H' not in neighbour_values):
                 return False
            elif card_value == 'V' and 'B' not in neighbour_values:  # or (card_value == 'B' and 'V' not in neighbour_values):
                 return False
            elif card_value == 'A' and 'V' in neighbour_values: # or (card_value == 'V' and 'A' not in neighbour_values):
                 return False

    return True

def print_board(board):
    print("._._{0}_.".format(board[0]))
    print("{0}_{1}_{2}_.".format(*board[1:4]))
    print("._{0}_{1}_{2}".format(*board[4:7]))
    print("._._{0}_.\n".format(board[7]))
    
iteration = 0
temp_board = board.copy()
for permutation in list(itertools.permutations(cards)):
    for i in range(0, len(permutation)):
        temp_board[i] = permutation[i]    
    iteration += 1
    if is_valid(temp_board): 
        print_board(list(temp_board.values()))
        print('number of iterations: {}'.format(iteration))
        break

calls = 1
def dfs_and_backtracking(temp_board, deck):
    global calls
    if is_valid(temp_board): 
        # base case where either board is full, or there no more available cards
        if '' not in list(temp_board.values()) or not deck:
            print_board(list(temp_board.values()))
            return True

        # assign a card of possible cards to index k and list all neighbours of card that are empty
        # position_neighbours = neighbours[k]
        possible_keys = [k for k in temp_board.keys() if temp_board[k] == '']
        
        for key in possible_keys:
            # place card down on position based on current deck 
            # and remove it from the deck
            for card in deck: 
                temp_board[key] = card
                updated_deck = deck.copy()
                updated_deck.remove(card)
                # add card to the puzzle and go step further in DFS
                calls += 1
                if dfs_and_backtracking(temp_board.copy(), updated_deck.copy()):
                    return True
            temp_board[key] = ''
    return False


dfs_and_backtracking(board.copy(), cards.copy())
print('recursive calls: {}:'.format(calls))