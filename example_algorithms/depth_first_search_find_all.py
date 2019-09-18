def find_all_paths(node, path=[]):
    path = path + [node]

    if is_goal(node):
        return [path]

    paths = [] # a list of paths

    for child in successors(node):
        # if not in current path
        if child not in path:
            # return list of paths from here
            newpaths = find_all_paths(child, path)
            # add every path found to paths
            for newpath in newpaths:
                paths.append(newpath)
    
    return paths