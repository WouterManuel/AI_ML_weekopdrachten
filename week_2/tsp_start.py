import itertools
import math
import random
import time
import matplotlib.pyplot as plt
from collections import namedtuple

# based on Peter Norvig's IPython Notebook on the TSP

City = namedtuple('City', 'x y')

def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)

def try_all_tours(cities):
    # generate and test all possible tours of the cities and choose the shortest tour
    tours = alltours(cities)
    return min(tours, key=tour_length)

def alltours(cities):
    # return a list of tours (a list of lists), each tour a permutation of cities,
    # and each one starting with the same city
    # cities is a set, sets don't support indexing
    start = next(iter(cities)) 
    return [[start] + list(rest)
            for rest in itertools.permutations(cities - {start})]

def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i-1]) 
               for i in range(len(tour)))

def make_cities(n, width=1000, height=1000):
    # make a set of n cities, each with random coordinates within a rectangle (width x height).

    random.seed(500) # the current system time is used as a seed
                  # note: if we use the same seed, we get the same set of cities

    return frozenset(City(random.randrange(width), random.randrange(height))
                     for c in range(n))

def plot_tour(tour): 
    # plot the cities as circles and the tour as lines between them
    points = list(tour) + [tour[0]]
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-')
    plt.axis('scaled') # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()

def plot_tsp(algorithm, cities):
    # apply a TSP algorithm to cities, print the time it took, and plot the resulting tour.
    t0 = time.process_time()
    tour = algorithm(cities)
    t1 = time.process_time()
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)

# opgave 1a 
def nearest_neighbor(cities):
    cnt_intersections = 0 # keep track of the amount of intersection in graph
    route = []
    unvisited = [city for city in cities]
    current = random.choice(unvisited) # select random city as starting point
    route.append(current)  
    unvisited.remove(current) # mark it as visited
    # total_length = 0
    print('starting node: {0}'.format(current))

    while len(unvisited) > 0: # while there are unvisited cities
        fastest_node = random.choice(unvisited) # choose random unvisited city to compare distance with
        shortest_dist = distance(current, fastest_node) # initialize shortest distance between A and B, to compare with
        
        if len(unvisited) > 1:  # if there is more than 1 vertex still to visit 
            for node in unvisited: # for each unvisited city)
                new_dist = distance(current, node)   
                if new_dist < shortest_dist: # if the distance is smaller than previously measured
                    shortest_dist = new_dist # shortest distance is now new found distance
                    fastest_node = node # and neighbor is now the fastest_node 
            new_line = (route[-1], fastest_node) # new line is drawn between last visited node and new found node
            # cnt_intersections += intersecting_with_path(route, new_line) # if new line is intersecting with existing path
            current = fastest_node # set current city to the nearest city
        else:   # if there is only one vertex left, it will connect to the starting point of our path
            # route.append(fastest_node) # add it to path sequence
            new_line = (fastest_node, route[0]) # new line is now drawn between last vertex and starting vertex
            # cnt_intersections += intersecting_with_path(route, new_line) # check if new line is intersecting with existing path

        route.append(fastest_node) # add it to path sequence
        unvisited.remove(fastest_node) # remove it from unvisited

    print('last node: {0}'.format(fastest_node))
    # print('number of intersections: {0}'.format(cnt_intersections))

    return route # return path
    
# implementation of 2-opt, applied on the path finding result of our implementation the nearest_neighbour algorithm.
# it finds intersections in the given path and swaps lines until local improvement is not increasing
# source for pseudo-code: https://en.wikipedia.org/wiki/2-opt
def two_opt(cities):
    # i =  maximum number of iterations, 
    route = nearest_neighbor(cities)
    route.append(route[0])
    best_route = route
    dist = tour_length(best_route)
    for i in range(0, len(route)-2): # index for line in route 
        for j in range(i+2, len(route)-1): # index for all other lines in route
            new_route = best_route[:] # best route 
            if is_intersection((best_route[i], best_route[i+1]), (best_route[j], best_route[j+1])):
                new_route[i+1:j+1] = best_route[j:i:-1] # swap edges in new route  
                new_dist = tour_length(new_route)
                if new_dist < dist: # check if new route is shorter than shortest route so far
                    best_route = new_route # shortest route is now new route
                    dist = new_dist
    return best_route

# function to check for intesections with a given path
# return the amount of intersections found 
def intersecting_with_path(path, new_line):
    if len(path) > 1:
        for i in range(0, len(path)-1): # check all segments of given path
            line_in_path = (path[i], path[i+1])
            if is_intersection(line_in_path, new_line): # if the new found line between parent and chosen node is causing an intersection
                # print('intersection found: {0}{1}'.format(line_in_path, new_line)) # let us know
                return True
    return False 

# source for finding intersection of lines: http://www.dcs.gla.ac.uk/~pat/52233/slides/Geometry1x1.pdf
def is_intersection(line_1, line_2):
    p1 = line_1[0]
    q1 = line_1[1]
    p2 = line_2[0]
    q2 = line_2[1]

    # if the lines share the same point, they are connected but not intersecting
    if p1 == p2 or q1 == q2 or p1 == q2 or p2 == q1:
        return False

    # check orientation of two lines (p1, q1, p2), (p1, q1, q2) 
    # and  (p2, q2, p1), (p2, q2, q1) are different
    # if so, there is an intersection 
    o1 = orientation(p1, q1, p2) 
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case 
    if o1 != o2 and o3 != o4: 
        return True
  
    return False

# source for deciding orientation: https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
def orientation(p1, p2, r):
    # calculate orientation of points
    o = (p2.y - p1.y) * (r.x - p2.x) - (r.y - p2.y) * (p2.x - p1.x)

    # is it colinear?
    if o == 0: 
        return 0
    # clock or counterclock wise  
    if o > 0:
        return 1
    else: 
        return 2

plot_tsp(nearest_neighbor, make_cities(100))
plot_tsp(two_opt, make_cities(500))