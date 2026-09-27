"""
data_fetcher.py
================
Builds a connected road-network graph for a selected USA region.
Uses:
  - Nominatim OpenStreetMap API for geocoding (coordinates)
  - OSRM Routing API for road driving distances

Saves the resulting graph to `map_data.json`.
"""

import requests
import json
import time

# 20 connected locations in the Chicago metropolitan area
LOCATIONS = [
    "Chicago, IL", "Evanston, IL", "Skokie, IL", "Des Plaines, IL", 
    "Rosemont, IL", "Oak Park, IL", "Cicero, IL", "Berwyn, IL", 
    "Elmhurst, IL", "Lombard, IL", "Downers Grove, IL", "Naperville, IL", 
    "Aurora, IL", "Joliet, IL", "Orland Park, IL", "Tinley Park, IL", 
    "Oak Lawn, IL", "Schaumburg, IL", "Elgin, IL", "Waukegan, IL"
]

def get_coordinates(city):
    """Fetch latitude and longitude using Nominatim API."""
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={city}"
    headers = {'User-Agent': 'CS411-Search-Visualizer-App'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and len(response.json()) > 0:
        data = response.json()[0]
        return float(data['lat']), float(data['lon'])
    print(f"Failed to fetch coordinates for {city}")
    return None, None

def get_driving_distance(coord1, coord2):
    """Fetch driving distance in meters using OSRM API."""
    # OSRM expects longitude,latitude
    url = f"http://router.project-osrm.org/route/v1/driving/{coord1[1]},{coord1[0]};{coord2[1]},{coord2[0]}?overview=false"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['code'] == 'Ok':
            return data['routes'][0]['distance']
    return float('inf')

def build_graph():
    graph_data = {"nodes": {}, "edges": {}}
    
    # 1. Fetch Coordinates
    print("Fetching coordinates...")
    for loc in LOCATIONS:
        lat, lon = get_coordinates(loc)
        if lat and lon:
            graph_data["nodes"][loc] = {"lat": lat, "lon": lon}
        time.sleep(1) # Respect Nominatim rate limits
        
    # 2. Build Connections (Simplifying to connect nearby cities to ensure connectivity)
    print("Building road network distances...")
    nodes = list(graph_data["nodes"].keys())
    
    for i in range(len(nodes)):
        loc1 = nodes[i]
        graph_data["edges"][loc1] = {}
        # Connect to the next 3 cities in the list to ensure a connected graph
        for j in range(1, 4):
            neighbor_idx = (i + j) % len(nodes)
            loc2 = nodes[neighbor_idx]
            
            # Avoid redundant API calls if edge already exists
            if loc2 in graph_data["edges"] and loc1 in graph_data["edges"][loc2]:
                distance = graph_data["edges"][loc2][loc1]
            else:
                coord1 = (graph_data["nodes"][loc1]["lat"], graph_data["nodes"][loc1]["lon"])
                coord2 = (graph_data["nodes"][loc2]["lat"], graph_data["nodes"][loc2]["lon"])
                distance = get_driving_distance(coord1, coord2)
                time.sleep(0.5) # Respect OSRM rate limits
                
            graph_data["edges"][loc1][loc2] = distance

    # 3. Save to map_data.json
    with open("map_data.json", "w") as f:
        json.dump(graph_data, f, indent=4)
    print("Graph successfully saved to map_data.json")

if __name__ == "__main__":
    build_graph()
