state_props = ["F", "G", "C", "W", "|"]
start_state = "FGCW|"
end_state = "|FGCW"
left_state = ""
right_state = ""
invalid_states = ("GW", "CG", "WG", "GW")
visited_states = []

def move_left(move): 
    left_state = move
    for state in possible_moves(left_state): 
        if state not in visited_states:
            visited_states.append(left_state + "|" + right_state)
            print(state)
            # move_right(move)
    
def move_right(move):
    right_state = move
    if is_safe(right_state):
        return True
    for state in possible_moves(right_state): 
        if state not in visited_states:
            visited_states.append(left_state + "|" + right_state)
            print(state)
            move_left(move)
    

# helper function for checking if given state is valid
def is_safe(side_state, move):
    if side_state not in invalid_states:
        visited_states.append(move)
        return True
    else:
        visited_states.append(move)
        return False


def reached_end_state(state):
    if state[0] == end_state[0] and all(prop in state for prop in end_state):
        return True
    else:
        return False


# successor function 
def possible_moves(state):
    possible_moves = ["F"]
    state.replace("F", "")
    if state != "": 
        for prop in state:
            if prop != "|" and prop != "F":
                possible_moves.append("F" + prop)
        return possible_moves
    else: 
        return possible_moves
        

# start state begins on leftside
move_left(start_state)
for move in visited_states: 
    print(move)

# 