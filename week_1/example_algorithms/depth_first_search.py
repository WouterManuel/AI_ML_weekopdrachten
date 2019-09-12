def dfs(node, visited):
    if is_goal(node):
        return True
    
    visited.add(node)
    for child in successors(node)
        if child not in visited:
            if dfs(child, visited):
                return True
                
    return False