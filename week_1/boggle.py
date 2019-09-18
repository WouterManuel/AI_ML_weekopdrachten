from random import choice
import copy
import os
import time

directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]
# if we want to look diagonally aswell use the below variable
# directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
board_size = 4

start_time = 0
elapsed_time = 0

# generates the x by x grid
def generate_board():
    board = []
    for i in range(0, board_size):
        board.append([])
        for j in range(0, board_size):
            board[i].append(random_letter())
    return board


#returns a random unicode character (65 through 90 is the alphabet)
def random_letter():
    return chr(choice(range(65,90)))


words_list = []
# loads the text file with words and puts it in a list
def load_dictionary():
    # had to define the directory name and path to the file otherwise it wouldnt find it
    this_folder = os.path.dirname(os.path.abspath(__file__))
    bestand = os.path.join(this_folder, 'words.txt')
    # the r means read
    with open(bestand, "r") as txt:
        for line in txt:
            words_list.append(line[:-1].upper())


def find_words(board):
    words = []
    for i in range(board_size):
        for j in range(board_size):
            # if the letter is not yet in our letters list, add it with the x/y coordinates of where we found it on the grid
            if board[i][j] not in letters:
                letters[board[i][j]] = []
            letters[board[i][j]].append((i, j))
            # look around the letter and add the adjacent letters + their x/y coordinates to a list
            adjacent_list[(board[i][j], i, j)] = []
            for x, y in directions:
                k = i+x
                l = j+y
                if k >= 0 and k < 4 and l >= 0 and l < 4:
                    adjacent_list[(board[i][j], i, j)].append((board[k][l], k, l))
    # call the dfs search for each word in the word list
    for word in words_list:
        if dfs(board, word):
            words.append(word)
    return words


letters = {}
adjacent_list = {}
def dfs(board,word):
    stack = []
    # if the first letter of the word does not exist in our board, end the search
    if word[0] not in (letters):
        return False
    # loop through the grid positions where we found the letter (can be multiple)
    for i, j in letters[word[0]]:
        # add the letter, complete word we are looking for, letter + x/y coordinates as a tuple and the x/y coordinates as a set to our stack
        stack.append((word[0], word, (word[0], i, j), set([(i, j)])))
    while len(stack) > 0:
        # pop the above mentioned information into 4 seperate variables
        sub, word, let, positions = stack.pop()
        # return if we finished making the word we are looking for (unlikely)
        if sub == word:
            return True
        next_letter = word[len(sub)]
        # for all letters adjacent to ours, get the letter and coordinates
        for l, i, j in adjacent_list[let]:
            # if one of the adjacent letters matches the next letter we are looking for (and its not our own letter) copy its position and add it to the stack
            if l == next_letter and (i, j) not in positions:
                p2 = copy.copy(positions)
                p2.add((i,j))
                stack.append((sub+next_letter, word, (l, i, j), p2))
    return False
    

def solve():
    start_time = time.time()
    load_dictionary()
    board = generate_board()
    words = find_words(board)
    elapsed_time = time.time() - start_time
    for row in board:
        print(row)
    for word in words:
        print("word " + word)
    print("time : " +  str(elapsed_time))

solve()