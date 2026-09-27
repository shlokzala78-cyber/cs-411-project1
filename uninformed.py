# uninformed.py
# BFS, DFS, UCS, and IDS
# I used a parent dictionary to rebuild the path at the end.

from collections import deque
import heapq

def bfs(graph, start, goal):
    # Breadth-First Search using a FIFO queue.
    queue = deque([(start, [start], 0)])
    visited = {start}
    expanded = 0
    
    while queue:
        node, path, cost = queue.popleft()
        expanded += 1
        
        if node == goal:
            return path, cost, expanded
            
        for neighbor, dist in graph['edges'].get(node, {}).items():
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor], cost + dist))
                
    return None, 0, expanded

def dfs(graph, start, goal):
    # Depth-First Search using a LIFO stack.
    stack = [(start, [start], 0)]
    visited = set()
    expanded = 0
    
    while stack:
        node, path, cost = stack.pop()
        
        if node not in visited:
            visited.add(node)
            expanded += 1
            
            if node == goal:
                return path, cost, expanded
                
            for neighbor, dist in graph['edges'].get(node, {}).items():
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor], cost + dist))
                    
    return None, 0, expanded

def ucs(graph, start, goal):
    # Uniform-Cost Search using a priority queue (min-heap) based on path cost.
    pq = [(0, start, [start])]
    visited = set()
    expanded = 0
    
    while pq:
        cost, node, path = heapq.heappop(pq)
        
        if node not in visited:
            visited.add(node)
            expanded += 1
            
            if node == goal:
                return path, cost, expanded
                
            for neighbor, dist in graph['edges'].get(node, {}).items():
                if neighbor not in visited:
                    heapq.heappush(pq, (cost + dist, neighbor, path + [neighbor]))
                    
    return None, 0, expanded

def ids(graph, start, goal, max_depth=50):
    # IDS combining DFS space efficiency with BFS completeness.
    def dls(node, path, cost, depth, visited):
        nonlocal expanded
        expanded += 1
        
        if depth == 0 and node == goal:
            return path, cost
        if depth > 0:
            for neighbor, dist in graph['edges'].get(node, {}).items():
                if neighbor not in visited:
                    visited.add(neighbor)
                    res_path, res_cost = dls(neighbor, path + [neighbor], cost + dist, depth - 1, visited)
                    if res_path:
                        return res_path, res_cost
                    visited.remove(neighbor)
        return None, 0

    expanded = 0
    for depth in range(max_depth):
        visited = {start}
        path, cost = dls(start, [start], 0, depth, visited)
        if path:
            return path, cost, expanded
            
    return None, 0, expanded
