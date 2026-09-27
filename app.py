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

# Concept notes mapped to algorithms
CONCEPT_NOTES = {
    'bfs': "Main Idea: Explores evenly level by level. Node Selection: FIFO (Queue), choosing the shallowest unexpanded node. Information Used: Depth only.",
    'dfs': "Main Idea: Dives as deep as possible before backtracking. Node Selection: LIFO (Stack), choosing the deepest unexpanded node. Information Used: Depth only.",
    'ucs': "Main Idea: Finds the cheapest path. Node Selection: Priority Queue based on lowest accumulated path cost g(n). Information Used: Path cost only.",
    'ids': "Main Idea: Combines BFS completeness with DFS space efficiency. Node Selection: Repeated DLS with increasing depth limits. Information Used: Depth only.",
    'greedy': "Main Idea: Rushes toward the goal blindly. Node Selection: Priority Queue based solely on heuristic distance h(n) to goal. Information Used: Heuristic only.",
    'astar': "Main Idea: Balances path cost and goal proximity for optimal routing. Node Selection: Priority Queue based on f(n) = g(n) + h(n). Information Used: Path cost and heuristic."
}

@app.route('/')
def index():
    nodes = list(graph['nodes'].keys())
    return render_template('index.html', nodes=nodes)

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    start, goal, algo = data['source'], data['destination'], data['algorithm']
    
    # Route to appropriate algorithm
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
        
    # Build coordinate array for the frontend map polyline
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
