import itertools
import random

# posities op het bord, volgens coordinaten in een 2D lijst
board = {0: '', 1: '', 2: '', 3: '',
         4: '', 5: '', 6: '', 7: ''}

# dict met alle aangrenzende posities per positie op het bord
neighbours = {0: [3], 1: [2], 2: [1, 3, 4], 3: [0, 2, 5], 
              4: [2, 5], 5: [3, 4, 6, 7], 6: [5], 7: [5]}

# alle mogelijke te spelen kaarten
cards = ['A', 'A', 'H', 'H', 'D', 'D', 'B', 'B']

# elke A grenst aan een H
# elke H grenst aan een D
# elke D grenst aan een B
# elke A grenst NIET aan een D
# twee kaarten van dezelfde soort mogen niet buren zijn

# for loop
def is_valid(k_board):
    for key in k_board.keys():
        card_value = k_board[key]
        list_neighbours= [x for x in neighbours[key]]
        neighbour_values = [k_board[v] for v in list_neighbours]

        if card_value in neighbour_values: 
            return False
        elif card_value == 'A' and 'H' not in neighbour_values:
            return False
        elif card_value == 'H' and 'D' not in neighbour_values:
            return False
        elif card_value == 'D' and 'B' not in neighbour_values:
            return False 
        elif card_value == 'A' and 'D' in neighbour_values:
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


def dfs(temp_board, available_cards, k):
    # base case 
    if not available_cards or k > len(temp_board):
        print_board(list(temp_board.values()))
        return list(temp_board)
    
    temp_board[k] = available_cards[0]

    for i in range(len(available_cards[1:])):
        temp_board[k+1] = available_cards[i]
        print('current board: {0}'.format(list(temp_board.values())))
        if is_valid(temp_board):
            print('board is valid')
            del available_cards[0]
            del available_cards[i]
            dfs(temp_board, available_cards, k+2)


dfs(board.copy(), cards.copy(), 0)