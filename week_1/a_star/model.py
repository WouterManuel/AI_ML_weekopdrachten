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
    # plot a sample path for demonstration
    for i in range(cf.SIZE-1):
        app.plot_line_segment(i, i, i, i+1, color=cf.FINAL_C)
        app.plot_line_segment(i, i+1, i+1, i+1, color=cf.FINAL_C)
        app.pause()

# voor de uitwerking van het UCS algoritme is het voorbeeld uit de sheets
# van het hoorcollege 1-2 gebruikt.
def ucs(app, start, goal): 
    pqueue = PriorityQueue()
    path = []
    visited = {}
    visited[start] = 0
    pqueue.put((start,path+[start]), 0)

    # loop through possible paths while the queue 
    while not pqueue.empty():
        item = pqueue.get() 
        prev_node = item[0]
        prev_cost = visited[prev_node]
        path = item[1]
        current = path[-1]

        if current == goal:
            return path
        
        for neighbour in neighbours(current):
            cost = prev_cost + 1
            if neighbour not in visited:
                visited[neighbour] = cost
                pqueue.put((current, path+[neighbour]), cost)
                app.plot_node(neighbour, color=cf.PATH_C)
        app.pause()
                
    app.path_not_found_message()            
    return path


# TODO: WERKT NIET OPTIMAAl, WE WETEN OOK NIET PRECIES WAAROM. GRAAG DIT OVERLEGGEN IN VRAGENUURTJE
def a_star(app, start, goal):
    pqueue = PriorityQueue()
    path = [] # keeps being added onto and will eventually return from function as shortest path
    visited = {} # keeps track of all visited nodes and their priority values
    pqueue.put((start, path+[start]), 0)
    visited[start] = 0

    # loop through possible paths while the queue is not empty
    while not pqueue.empty():
        item = pqueue.get() 
        parent = item[0]
        path = item[1]
        prev_cost = visited[parent]
        current = path[-1] 
        print("current path {0} with priority {1}".format(current, prev_cost))

        if current == goal:
            return path
        
        for neighbour in neighbours(current):
                g = prev_cost + 1
                h = cost(neighbour, goal) # heuristic
                p = g + h # priority = g + h
                # or (neighbour in visited and not visited[neighbour] > visited[current])
                if neighbour not in visited or g < prev_cost:
                    visited[neighbour] = g # node has now been visited
                    print("     p for neighbour {0} is {1}".format(neighbour, p))
                    pqueue.put((current, path+[neighbour]), p) # add neighbour to queue
                    app.plot_node(neighbour, color=cf.PATH_C)
                    app.pause() # pause loop according to set delay
    
    app.path_not_found_message()            
    return path

# calculates cost based on heuristic
# source for chosen heuristic: https://www.kdnuggets.com/2017/08/comparing-distance-measurements-python-scipy.html
def cost(n1, n2):
    x1 = n1[0]
    y1 = n1[1]
    x2 = n2[0]
    y2 = n2[1]
    # Euclidian distance. allows for diagonal measurement of distance
    return math.sqrt(abs((x2-x1)**2) + abs((y2-y1)**2))

# helper function that checks all possible neighbours for a given node
def neighbours(node):
    x = node[0]
    y = node[1]
    # directions: left, right, up, down
    directions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    neighbours = []
    for direction in directions:
        if not out_of_bounds(direction) and not_blocked(direction):
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
        return True
    else:
        return False

