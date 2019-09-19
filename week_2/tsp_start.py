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

    random.seed(1000) # the current system time is used as a seed
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
    t0 = time.clock()
    tour = algorithm(cities)
    t1 = time.clock()
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)

# opgave 1a 
def nearest_neighbor(cities):
    shortest_path = []
    unvisited = [x for x in cities]
    current = random.choice(unvisited)              # select random city as starting point
    shortest_path.append(current)  
    unvisited.remove(current)                       # mark it as visited
    while len(unvisited) != 0:                      # while there are unvisited cities
        fastest_node = random.choice(unvisited)     # initialize shortest distance between A and B to 0
        shortest_dist = distance(current, fastest_node)
        for city in unvisited:                      # for each unvisited city 
            new_dist = distance(current, city)   
            if new_dist < shortest_dist:            # if the distance is the smaller than previously measured
                shortest_dist = new_dist            # shortest distance is now new found distance
                fastest_node = city                 # and neighbor is now the fastest_node    
        shortest_path.append(fastest_node)          # add it to path sequence
        unvisited.remove(fastest_node)              # remove it from unvisited
        current = fastest_node                      # set current city to the nearest city
    return shortest_path                            # return shortest path

def find_intersections

plot_tsp(nearest_neighbor, make_cities(100))
