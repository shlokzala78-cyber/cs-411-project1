# app.py
# Flask server backend and API endpoints
# I used a dictionary mapping to route the frontend requests to the correct search algorithm functions.

from flask import Flask, render_template, request, jsonify
import json
import uninformed
import informed

app = Flask(__name__)

# Load map data at startup
with open('map_data.json', 'r') as f:
    graph = json.load(f)

# Concept notes updated to dictionaries for structured card rendering
CONCEPT_NOTES = {
    'bfs': {
        'main_idea': "Explores evenly level by level.",
        'node_selection': "FIFO (Queue), choosing the shallowest unexpanded node.",
        'info_used': "Depth only."
    },
    'dfs': {
        'main_idea': "Dives as deep as possible before backtracking.",
        'node_selection': "LIFO (Stack), choosing the deepest unexpanded node.",
        'info_used': "Depth only."
    },
    'ucs': {
        'main_idea': "Finds the cheapest path by expanding the lowest cost node.",
        'node_selection': "Priority Queue based on lowest accumulated path cost g(n).",
        'info_used': "Actual cost g(n) only."
    },
    'ids': {
        'main_idea': "Combines BFS completeness with DFS space efficiency.",
        'node_selection': "Repeated DLS with increasing depth limits.",
        'info_used': "Depth only."
    },
    'greedy': {
        'main_idea': "Rushes toward the goal blindly based on estimated proximity.",
        'node_selection': "Priority Queue based solely on heuristic distance h(n) to goal.",
        'info_used': "Heuristic estimate h(n) only."
    },
    'astar': {
        'main_idea': "Finds the shortest path balancing actual cost g(n) and estimated cost h(n).",
        'node_selection': "Selects node with minimum f(n) = g(n) + h(n).",
        'info_used': "Actual cost g(n) and heuristic estimate h(n)."
    }
}

@app.route('/')
def index():
    nodes = list(graph['nodes'].keys())
    return render_template('index.html', nodes=nodes, graph_data=graph)

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    start, goal, algo = data['source'], data['destination'], data['algorithm']
    
    algo_map = {
        'bfs': uninformed.bfs,
        'dfs': uninformed.dfs,
        'ucs': uninformed.ucs,
        'ids': uninformed.ids,
        'greedy': informed.greedy,
        'astar': informed.astar
    }
    
    if algo not in algo_map:
        return jsonify({"error": "Invalid algorithm"}), 400
        
    path, cost, expanded = algo_map[algo](graph, start, goal)
    
    if not path:
        return jsonify({"error": "No path found."})
        
    path_coords = [{"lat": graph['nodes'][node]['lat'], "lon": graph['nodes'][node]['lon']} for node in path]
    
    return jsonify({
        "path": path,
        "cost": round(cost, 2),
        "expanded": expanded,
        "coords": path_coords,
        "note": CONCEPT_NOTES[algo]
    })

if __name__ == '__main__':
    app.run(debug=True)
