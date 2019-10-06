import random
import itertools
import math

MAX_DEPTH = 3

def merge_left(b):
    # merge the board left
    # this is the funcyoin that is reused in the other merges
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]    
    def merge(row, acc):
        # recursive helper for merge_left

        # if len row == 0, return accumulator
        if not row:
            return acc

        # x = first element
        x = row[0]
        # if len(row) == 1, add element to accumulator
        if len(row) == 1:
            return acc + [x]

        # if len(row) >= 2
        if x == row[1]:
            # add row[0] + row[1] to accumulator, continue with row[2:]
            return merge(row[2:], acc + [2 * x])
        else:
            # add row[0] to accumulator, continue with row[1:]
            return merge(row[1:], acc + [x])

    new_b = []
    for row in b:
        # merge row, skip the [0]'s
        merged = merge([x for x in row if x != 0], [])
        # add [0]'s to the right if necessary
        merged = merged + [0] * (len(row) - len(merged))
        new_b.append(merged)
    # return [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    return new_b

def merge_right(b):
    # merge the board right
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    def reverse(x):
        return list(reversed(x))

    # rev = [[4, 4, 2, 0], [8, 4, 2, 0], [4, 0, 0, 0], [2, 2, 2, 2]]
    rev = [reverse(x) for x in b]
    # ml = [[8, 2, 0, 0], [8, 4, 2, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    ml = merge_left(rev)
    # return [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    return [reverse(x) for x in ml]


def merge_up(b):
    # merge the board upward
    # note that zip(*b) is the transpose of b
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    # trans = [[2, 0, 0, 0], [4, 2, 0, 0], [8, 2, 0, 0], [4, 8, 4, 2]]
    trans = merge_left(zip(*b))
    # return [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    return [list(x) for x in zip(*trans)]


def merge_down(b):
    # merge the board downward
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    # trans = [[0, 0, 0, 2], [0, 0, 2, 4], [0, 0, 8, 2], [4, 8, 4, 2]]
    trans = merge_right(zip(*b))
    # return [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    return [list(x) for x in zip(*trans)]


# location: after functions
MERGE_FUNCTIONS = {
    'left': merge_left,
    'right': merge_right,
    'up': merge_up,
    'down': merge_down
}

def move_exists(b):
    # check whether or not a move exists on the board
    # b = [[1, 2, 3, 4], [5, 6, 7, 8]]
    # move_exists(b) return False
    def inner(b):
        for row in b:
            for x, y in zip(row[:-1], row[1:]):

                # tuples (1, 2),(2, 3),(3, 4),(5, 6),(6, 7),(7, 8)
                if x == y or x == 0 or y == 0:
                    return True
        return False

    if inner(b) or inner(zip(*b)):
        return True
    else:
        return False

def start():
    # make initial board
    b = [[0] * 4 for _ in range(4)]
    add_two_four(b)
    add_two_four(b)
    return b


def play_move(b, direction):
    # get merge functin an apply it to board
    b = MERGE_FUNCTIONS[direction](b)
    add_two_four(b)
    return b


def add_two_four(b):
    # add a random tile to the board at open position.
    # chance of placing a 2 is 90%; chance of 4 is 10%
    rows, cols = list(range(4)), list(range(4))
    random.shuffle(rows)
    random.shuffle(cols)
    distribution = [2] * 9 + [4]
    for i, j in itertools.product(rows, rows):
        if b[i][j] == 0:
            b[i][j] = random.sample(distribution, 1)[0]
            return (b)
        else:
            continue

def game_state(b):
    for i in range(4):
        for j in range(4):
            if b[i][j] >= 2048:
                return 'win'
    return 'lose'

def test():
    b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    assert merge_left(b) == [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    assert merge_right(b) == [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    assert merge_up(b) == [(2, 4, 8, 4), (0, 2, 2, 8), (0, 0, 0, 4), (0, 0, 0, 2)]
    assert merge_down(b) == [(0, 0, 0, 4), (0, 0, 0, 8), (0, 2, 8, 4), (2, 4, 2, 2)]
    assert move_exists(b) == True
    b = [[2, 8, 4, 0], [16, 0, 0, 0], [2, 0, 2, 0], [2, 0, 0, 0]]
    assert (merge_left(b)) == [[2, 8, 4, 0], [16, 0, 0, 0], [4, 0, 0, 0], [2, 0, 0, 0]]
    assert (merge_right(b)) == [[0, 2, 8, 4], [0, 0, 0, 16], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert (merge_up(b)) == [(2, 8, 4, 0), (16, 0, 2, 0), (4, 0, 0, 0), (0, 0, 0, 0)]
    assert (merge_down(b)) == [(0, 0, 0, 0), (2, 0, 0, 0), (16, 0, 4, 0), (4, 8, 2, 0)]
    assert (move_exists(b)) == True
    b = [[0, 7, 0, 0], [0, 0, 7, 7], [0, 0, 0, 7], [0, 7, 0, 0]]
    g = Game()
    for i in range(11):
        g.add_two_four(b)

def get_random_move():
    return random.choice(list(MERGE_FUNCTIONS.keys()))

def expectimax(b, turn, depth=0):
    alpha = 0

    # base case: return heuristic value of node
    if depth == MAX_DEPTH:
        alpha += (upper_left(b) + smoothness(b))*math.sqrt(empty_spaces(b))
        return alpha

    if turn == True:
        for move in MERGE_FUNCTIONS.keys():
            alpha += max(alpha, expectimax(MERGE_FUNCTIONS[move](b), False, depth + 1))
        return alpha

    else: 
        # used to map all zeros in the given board
        zeros = [(i,j) for i , j in itertools.product(range(4), range(4)) if b[i][j] == 0]
        # for every zero on zeros
        for i, j in zeros:
            # generate two baord based on the position of a mapped zero in a given board
            b1 = [x[:] for x in b]
            b2 = [x[:] for x in b]
            # for every mapped zero lace either a 2 or a 4 in this position
            b1[i][j] = 2
            b2[i][j] = 4
            
            # for the newly made boards sum up the scores of them, taking their expectancy into account
            alpha += math.floor((.9 * expectimax(b1, True, depth + 1) / len(zeros)) + (.1 * expectimax(b2, True, depth + 1) / len(zeros)))
        
        return alpha # return calculated average

def get_expectimax_move(b):
    direction_values = {'left': 0, 'right': 0, 'up': 0, 'down': 0}
    for direction in direction_values.keys():
        direction_values[direction] = expectimax(MERGE_FUNCTIONS[direction](b), False, 0)
    print(direction_values)
    # return the direction with the highest score
    print(max(direction_values.keys(), key=lambda k: direction_values[k]))
    return max(direction_values.keys(), key=lambda k: direction_values[k]) 


# heuristic to give the upper left corner the highest priority
def upper_left(b):
    weight =    [   [2048, 256, 16, 1],
                    [512, 128, 1, 1],
                    [256, 4, 1, 1],
                    [64, 2, 1, 1]]

    total_value = 0
    for x in range(4):
        for y in range(4):
            total_value += b[x][y] * weight[x][y]
    return total_value


# heuristic to give the upper left corner the highest priority for biggest value on board
def empty_spaces(b):
    number_of_empty_spaces = 1
    for x in range(4):
        for y in range(4): 
            if b[x][y] == 0:
                number_of_empty_spaces = number_of_empty_spaces * 2
    return number_of_empty_spaces

# heuristic to give boards with highest numbers on boards the biggest priority
def max_value(b):
    max_value = 0
    for x in range(4):
        for y in range(4): 
            if b[x][y] > max_value:
                max_value = b[x][y]
    return max_value

def smoothness(b):
    smoothness_score = 1
    for x in range(4):
        for y in range(4): 
            if b[x][y] != 0:
                if x != 3:
                    if y != 3:
                        if b[x][y] == b[x][y+1]:
                            smoothness_score += 2
                        if b[x][y] == b[x+1][y]:
                            smoothness_score += 2
                        if b[x][y] == b[x+1][y+1]:
                            smoothness_score += 2
                    if y == 3:
                        if b[x][y] == b[x+1][y]:
                            smoothness_score += 2
                if x == 3:
                    if y == 0:
                        if b[x][y] == b[x][y+1]:
                            smoothness_score += 2
                    if y == 3:
                        if b[x][y] == b[x-1][y]:
                            smoothness_score += 2 
    return smoothness_score