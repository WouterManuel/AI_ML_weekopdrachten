import random
import heapq
import math
import config as cf

# global var
grid  = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]

class PriorityQueue:
    # to be use in the A* algorithm
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
        return heapq.heappop(self.elements)[1]

def bernoulli_trial(app):
    return 1 if random.random() < int(app.prob.get())/10 else 0

def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    return grid[node[0]][node[1]]

def set_grid_value(node, value): 
    # node is a tuple (x, y), grid is a 2D list [x][y]
    grid[node[0]][node[1]] = value

def search(app, start, goal):
    USC(app, start, goal)
    # # plot a sample path for demonstration
    # for i in range(cf.SIZE-1):
    #     app.plot_line_segment(i, i, i, i+1, color=cf.FINAL_C)
    #     app.plot_line_segment(i, i+1, i+1, i+1, color=cf.FINAL_C)
    #     app.pause()

def USC(app, start, goal):
    # if current pos = goal return done
    frontier = PriorityQueue()
    visited = set()
    for x in range(5):
        for y in range(5):
            get_next_possible_moves(app, (x, y))
            app.pause()
    # cost = start post - mijn pos en dan de X + Y doen 
    # frontier.put(start, 0)
    # define a 

def get_next_possible_moves(app, node):
    # node = 5, 5
    x = node[0]
    y = node[1] 
    print("grid value of node {1} is : {0}".format(get_grid_value(node), node))
    if(get_grid_value((x+1, y)) != "b"):
        app.plot_line_segment(x, y, x+1, y, color=cf.PATH_C)
        print("from node : {0} to {1} , {2}".format(node, x+1, y))
    if(get_grid_value((x-1, y)) != "b"):
        app.plot_line_segment(x, y, x-1, y, color=cf.PATH_C)
        print("from node : {0} to {1} , {2}".format(node, x-1, y))
