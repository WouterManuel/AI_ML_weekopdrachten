start_state = "CFGW|"

# all permutations of the goal state, just in case...
end_state = "|CFGW"

# all permutations of invalid states, just in case...
invalid = ("GW","CG", "CGW")

# to find the paths recursively I used the example given in the AI lecture sheets 1.1
def move_actor(move, side, path=[]):
    path = path + [move]
    left_state = state_string_filter(move, 0)
    right_state = state_string_filter(move, 1)        
    paths = []

    if goal_state(move):
        return [path]

    # move actors to the right side 
    if side is "right":
        # check all possible moves from current state
        for possible_move in possible_moves(right_state, side): 
            # set a temporary valuable to hold the state of the right side
            temp_right = right_state
            # remove all actors in possible move from the temporary right side
            for actor in possible_move:
                if actor in temp_right:
                    temp_right = temp_right.replace(actor, "")

            # put together a string representing a new temporary state
            temp_state = ''.join(sorted(possible_move + left_state)) + "|" + ''.join(sorted(temp_right))

            # checks if the new temporary found state has not already been visited
            if temp_state not in path:
                # check if the state of the right side (after making the move) is a safe side
                if is_safe(temp_right) == False:
                    # add the temp state to "visited" states
                    print("illegal state '{0}': {1}".format(temp_right, temp_state))
                    path.append(temp_state)
                    paths.append(path)
                # else, explore the treated by the valid move
                else:
                    newpaths = move_actor(temp_state, "left", path)
                    for newpath in newpaths:
                        paths.append(newpath)

    # move actors to the left side 
    elif side is "left": 
        for possible_move in possible_moves(left_state, side):
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
                    paths.append(path)
                else:
                    newpaths = move_actor(temp_state, "right", path)
                    for newpath in newpaths:
                        paths.append(newpath)
    return paths


# helper function for checking if given state is valid
def is_safe(side_state):
    if side_state in invalid:
        return False
    else:
        return True


# check if endstage is reached
def goal_state(state):
    if state == end_state:
        return True
    else:
        return False

# successor function 
def possible_moves(state, side):
    possible_moves = []
    if len(state) < 4 and side == "right": 
        if len(state) >= 2:
            possible_moves.append("F")
            return possible_moves
    else:
        for actor in state:
            if actor != "F":
                possible_moves.append("F" + actor) 
    return possible_moves


# helper function that filters out the state of the river side that calls it
def state_string_filter(move, num):
    # side_state = move
    temp_move = move.split("|",1)[num]
    # if len(temp_move) > 0:
    #     for actor in temp_move: 
    #        side_state += actor
    return temp_move

# start state begins on leftside
print(start_state)
print("final result: {0}".format(move_actor(start_state, "left")))
