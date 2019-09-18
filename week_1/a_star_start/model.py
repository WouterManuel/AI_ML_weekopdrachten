import random
import heapq
import math
import config as cf

# global var
grid  = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]

class PriorityQueue:
    # to be used in the A* algorithm
    # a wrapper around heapq (aka priority queue), a binary min-heap on top of a list
    # in a min-heap, the keys of parent nodes are less than or equal to those
    # of the children and the lowest key is in the root node
    def __init__(self):
        # create a min heap (as a list)
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    # heap elements are tuples (priority, item)
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    # pop returns the smallest item from the heap
    # i.e. the root element = element (priority, item) with highest priority
    def get(self):
        return heapq.heappop(self.elements)

def bernoulli_trial(app):
    return 1 if random.random() < int(app.prob.get())/10 else 0

def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    return grid[node[0]][node[1]]

def set_grid_value(node, value): 
    # node is a tuple (x, y), grid is a 2D list [x][y]
    grid[node[0]][node[1]] = value

def search(app, start, goal):
    # plot a sample path for demonstration
    for i in range(cf.SIZE-1):
        app.plot_line_segment(i, i, i, i+1, color=cf.FINAL_C)
        app.plot_line_segment(i, i+1, i+1, i+1, color=cf.FINAL_C)
        app.pause()

# voor de uitwerking van het UCS algoritme is het voorbeeld uit de sheets\
# van het hoorcollege 1-2 gebruikt.
def ucs(app, start, goal): 
    pqueue = PriorityQueue()
    path = []
    visited = set()
    pqueue.put((start,path+[start]), 0)

    while not pqueue.empty():
        cumulative_cost, item = pqueue.get() 
        current_node = item[0]
        path = item[1]

        if current_node == goal:
            return path

        for neighbour in neighbours(current_node):
            if neighbour not in visited:
                pqueue.put((neighbour, path+[neighbour]), cumulative_cost+1)
                visited.add(neighbour)
                if neighbour != goal: 
                    app.plot_node(neighbour, color=cf.PATH_C)
                app.pause()
                
    app.path_not_found_message()            
    return path
    
# helper function that checks all possible neighbours for a given node
def neighbours(node):
    x = node[0]
    y = node[1]
    # directions: left, right, up, down
    directions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    neighbours = []
    
    for direction in directions:
        if out_of_bounds(direction):
            if not_blocked(direction):
                neighbours.append(direction)

    return neighbours

# helper function that checks if a node is blocked
def not_blocked(node):
    if get_grid_value(node) == -1:
        return True
    else:
        return False


# helper function that checks if a coordinate is out of bounds 
def out_of_bounds(node):
    # compare coordinates with size of board or if they are smaller than 0
    if node[0] > cf.SIZE-1 or node[1] > cf.SIZE-1 or node[0] < 0 or node[1] < 0:
        return False
    else:
        return True

