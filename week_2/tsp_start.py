import matplotlib.pyplot as plt
import random
import time
import itertools
import math
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

def get_neighbours(cities):
    shortest_path = []
    unvisited = [x for x in cities]
    current = random.choice(unvisited)
    unvisited.remove(current)
    shortest_path.append(current)

    while len(unvisited) != 0:
        fastest_node = random.choice(unvisited)
        shortest_distance = distance(current, fastest_node)
        for city in unvisited:
            dist = distance(current, city)
            if dist <= shortest_distance:
                shortest_distance = dist
                fastest_node = city
            # kijk bij alle bestaande lijnen of de lijn die we nu nieuw willen tekenen niet ermee intersect
            # for short_path in range(0, len(shortest_path)-1): #
            #     print(short_path)
        shortest_path.append(fastest_node)
        unvisited.remove(fastest_node)
        current = fastest_node
    return shortest_path

def orientation(p1, q1, p2):
    p1x = p1[0]
    p1y = p1[1]
    q1x = q1[0]
    q1y = q1[1]
    p2x = p2[0]
    p2y = p2[1]
    value = (q1y -p1x) * (p2x - q1x) - (q1x - p1x) * (p2y - q1y)
    if (value == 0): #colinear
        print("colinear orientation found, returning 0")
        return 0
    if value > 0: #clockwise
        return 1
    else:
        return 2 #counter clockwise

    return 


def intersect(p1, q1, p2, q2): 
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4: #intersection found
        return true

    return false
plot_tsp(get_neighbours, make_cities(10))
# plot_tsp(try_all_tours, make_cities(10))

# 1A: de optimale route met seed 1000 is 2403.1, 
# het NN algoritme geeft een route met lengte 2643.7 aan. NN ligt dus ongeveer 10% van optimale route af

# 1B: 0.121 seconde met een lengte van 21059.7

