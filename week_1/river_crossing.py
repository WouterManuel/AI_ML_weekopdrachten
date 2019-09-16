from itertools import permutations

start_state = "FCGW|"
# all permutations of the goal state, just in case
end_state = ["|FCGW","|FCWG","|FGCW","|FGWC","|FWCG","|FWGC","|CFGW","|CFWG",
            "|CGFW","|CGWF","|CWFG","|CWGF","|GFCW","|GFWC","|GCFW","|GCWF",
            "|GWFC","|GWCF","|WFCG","|WFGC","|WCFG","|WCGF","|WGFC","|WGCF"]
count = 0

# invalid states can be done differently, i.e 
# applying a helper function that checks if a chosen move will create a state wherein 
# two incompatible actors are situated. (for-loop with if statements) 
invalid = ("WG","GW","GC","CG","WGC","WCG","GWC","GCW","CWG","CGW")

#def find_all_solutions(state, path=[]):
#        path = path + [state]
#
#        if goal_state(state):
#            return [path]
#        
#        paths = [] # a list of paths
#
#        for child in successor(state):
#            if child not in path:
#                # return list of paths from here
#                newpaths = find_all_solutions(child, path)
#                # add every path found to paths
#                for newpath in newpaths:
#                    paths.append(newpath)
#        
#        return paths


def move_left(move, path=[]): 
    global count
    path = path + [move]
    left_state = state_string_filter(move, 0)
    right_state = state_string_filter(move, 1)
    paths = []

    if goal_state(move):
        return [path]

    for possible_move in possible_moves(left_state): 
        temp_left = left_state
        if possible_move not in path:
            for actor in possible_move:
                if actor in temp_left:
                    temp_left  = temp_left.replace(actor, "")

            # puts together a string representing a new temporary state 
            temp_state = temp_left  + "|" + possible_move + right_state 

            if is_safe(temp_left) is False:
                print("illegal state '{0}': {1}".format(temp_left, temp_state))
            # Add new valid temporary state to list of visited states
            # visited.append(current_state)
            else:
                print("boat to right {0}: {1}".format(count, possible_move))
                print("new state {0}: {1}".format(count, temp_state))
                count += 1
                newpaths = move_right(temp_state)
                print(newpaths)
                for newpath in newpaths:
                    paths.append(newpath)
    
    return paths


def move_right(move, path=[]):
    global count
    path = path + [move]
    left_state = state_string_filter(move, 0)
    right_state = state_string_filter(move, 1)        
    paths = []

    if goal_state(move):
        return [path]

    for possible_move in possible_moves(right_state): 
        temp_right = right_state
        if possible_move not in path:
            for actor in possible_move:
                if actor in temp_right:
                    temp_right = temp_right.replace(actor, "")

            # puts together a string representing a new temporary state 
            temp_state = possible_move + left_state + "|" + temp_right
            if is_safe(temp_right) is False:
                print("illegal state '{0}': {1}".format(temp_right, temp_state))
            # Add new valid temporary state to list of visited states
            # visited.append(current_state)
            else:
                print("boat to left {0}: {1}".format(count, possible_move))
                print("new state {0}: {1}".format(count, temp_state))
                count += 1
                newpaths = move_left(temp_state)
                print(newpaths)
                for newpath in newpaths:
                    paths.append(newpath)

    return paths


def move_actor(move, side, path=[]):
    global count
    path = path + [move]
    left_state = state_string_filter(move, 0)
    right_state = state_string_filter(move, 1)        
    paths = []

    if goal_state(move):
        print("WIN!")
        return [path]
#
    if count > 10:
        print("RAN OUT OF TIME")
        return paths

    # move actors to the right side 
    if side is "right":

        # check all possible moves from current state
        for possible_move in possible_moves(right_state, left_state): 

            # set a temporary valuable to hold the state of the right side
            temp_right = right_state

            # remove all actors in possible move from the temporary right side
            for actor in possible_move:
                if actor in temp_right:
                    temp_right = temp_right.replace(actor, "")

            # put together a string representing a new temporary state
            # based on the current possible move and combine it into a string together with the state of left 
            # and temporary state of right, to represent a new temporary state.
            temp_state = ''.join(sorted(possible_move + left_state)) + "|" + ''.join(sorted(temp_right))

            # checks if the new temporary found state has not already been visited
            if temp_state not in path:
                # check if the state of the right side (after making the move) is a safe side
                if is_safe(temp_right) == False:
                    print("illegal state '{0}': {1}".format(temp_right, temp_state))
                    # add the temp state to "visited" states
                    path.append(temp_state)

                # else, explore the treated by the valid move\
                else:
                    print("boat to left {0}: {1}".format(count, possible_move))
                    print("new state {0}: {1}".format(count, temp_state))
                    count += 1
                    newpaths = move_actor(temp_state, "left", path)
                    for newpath in newpaths:
                        paths.append(newpath)

    # move actors to the left side 
    elif side is "left": 
        for possible_move in possible_moves(left_state, right_state):
            temp_left = left_state

            for actor in possible_move:
                if actor in temp_left:
                    temp_left  = temp_left.replace(actor, "")

            # puts together a string representing a new temporary state 
            temp_state = ''.join(sorted(temp_left)) + "|" + ''.join(sorted(possible_move + right_state)) 

            if temp_state not in path:
                if is_safe(temp_left) == False:
                    print("illegal state '{0}': {1}".format(temp_left, temp_state))
                    path.append(temp_state)

                else:
                    print("boat to right {0}: {1}".format(count, possible_move))
                    print("new state {0}: {1}".format(count, temp_state))
                    count += 1
                    newpaths = move_actor(temp_state, "right", path)
                    for newpath in newpaths:
                        paths.append(newpath)
    
    # TODO: CHECK HOW STATES ARE ADDED TO PATH AND PATHS
    print("{0}: {1}".format(count, path))
    return paths


# helper function for checking if given state is valid
def is_safe(side_state):
    if side_state in invalid:
        return False
    else:
        return True


# check if endstage is reached
def goal_state(state):
    if state in end_state:
        return True
    else:
        return False


# helper function that filters out the state of the river side that calls it
def state_string_filter(move, num):
    # side_state = move
    temp_move = move.split("|",1)[num]
    # if len(temp_move) > 0:
    #     for actor in temp_move: 
    #        side_state += actor
    return temp_move


# successor function 
def possible_moves(state, safe_side):
    possible_moves = []
    if "F" in state: 
        if len(state) == 2 and is_safe(safe_side):
            possible_moves.append("F")
            return possible_moves

        elif len(state) == 2: 
            possible_moves.append(state)
            return possible_moves

        else:
            for actor in state:
                if actor != "F":
                    possible_moves.append("F" + actor)
            return possible_moves
    else: 
        return possible_moves


# start state begins on leftside
print(start_state)
print(move_actor(start_state, "left"))
