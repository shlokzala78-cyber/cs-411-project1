# informed.py
# Greedy Best-First Search and A*
# I used the Haversine formula to calculate the straight-line geographic distance as the heuristic.

import heapq
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8  # Radius of earth in miles (Changed from 6371000 meters)
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def get_h(graph, node, goal):
    # Heuristic function: straight-line distance to goal.
    n_data, g_data = graph['nodes'][node], graph['nodes'][goal]
    return haversine(n_data['lat'], n_data['lon'], g_data['lat'], g_data['lon'])

def greedy(graph, start, goal):
    # Greedy Best-First Search prioritizing nodes closest to the goal (h(n)).
    pq = [(get_h(graph, start, goal), start, [start], 0)]
    visited = set()
    expanded = 0
    
    while pq:
        _, node, path, cost = heapq.heappop(pq)
        
        if node not in visited:
            visited.add(node)
            expanded += 1
            
            if node == goal:
                return path, cost, expanded
                
            for neighbor, dist in graph['edges'].get(node, {}).items():
                if neighbor not in visited:
                    h = get_h(graph, neighbor, goal)
                    heapq.heappush(pq, (h, neighbor, path + [neighbor], cost + dist))
                    
    return None, 0, expanded

def astar(graph, start, goal):
    # A* Search minimizing the total estimated path cost (f(n) = g(n) + h(n)).
    pq = [(get_h(graph, start, goal), 0, start, [start])]
    visited = {}
    expanded = 0
    
    while pq:
        f, cost, node, path = heapq.heappop(pq)
        
        if node not in visited or cost < visited[node]:
            visited[node] = cost
            expanded += 1
            
            if node == goal:
                return path, cost, expanded
                
            for neighbor, dist in graph['edges'].get(node, {}).items():
                new_cost = cost + dist
                f_new = new_cost + get_h(graph, neighbor, goal)
                heapq.heappush(pq, (f_new, new_cost, neighbor, path + [neighbor]))
                
    return None, 0, expanded
