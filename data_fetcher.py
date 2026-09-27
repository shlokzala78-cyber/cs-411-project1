"""
data_fetcher.py
================
Builds a connected road-network graph for a selected USA region.
Uses:
  - Nominatim OpenStreetMap API for geocoding (coordinates)
  - OSRM Routing API for road driving distances

Saves the resulting graph to `map_data.json`.
"""

import json
import time
import math
import requests

REGION_NAME = "Illinois, USA"

# A distinct list of 22 locations around Chicago
CITIES = [
    "Chicago, IL", "Evanston, IL", "Oak Park, IL", "Cicero, IL",
    "Oak Lawn, IL", "Des Plaines, IL", "Arlington Heights, IL",
    "Schaumburg, IL", "Elk Grove Village, IL", "Palatine, IL",
    "Glenview, IL", "Northbrook, IL", "Highland Park, IL",
    "Waukegan, IL", "Gurnee, IL", "Libertyville, IL",
    "Mundelein, IL", "Vernon Hills, IL", "Naperville, IL",
    "Aurora, IL", "Wheaton, IL", "Downers Grove, IL"
]

def get_coords(city):
    """Fetch latitude and longitude using Nominatim."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city, "format": "json", "limit": 1}
    headers = {"User-Agent": "CS411-IntelligentSearch-App"}
    
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        if resp.status_code == 200 and resp.json():
            return float(resp.json()[0]["lat"]), float(resp.json()[0]["lon"])
    except Exception as e:
        print(f"Failed to geocode {city}: {e}")
    return None, None

def get_route_distance(lat1, lon1, lat2, lon2):
    """Fetch driving distance in miles using OSRM."""
    url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("code") == "Ok":
                # Convert meters to miles
                return round(data["routes"][0]["distance"] * 0.000621371, 2)
    except Exception as e:
        print(f"OSRM routing failed: {e}")
    return 999.99  # Fallback error distance

def build_graph():
    graph = {"nodes": {}, "edges": {}}
    
    print(f"Building map graph for: {REGION_NAME}")
    print("Step 1: Geocoding cities...")
    
    for city in CITIES:
        lat, lon = get_coords(city)
        if lat and lon:
            graph["nodes"][city] = {"lat": lat, "lon": lon}
            print(f"  Located: {city}")
        time.sleep(1) # Respect Nominatim 1-second rate limit policy

    print("\nStep 2: Dynamically connecting nearest neighbors...")
    node_names = list(graph["nodes"].keys())
    
    # Initialize edge dictionaries
    for city in node_names:
        graph["edges"][city] = {}
        
    for city_a in node_names:
        lat_a, lon_a = graph["nodes"][city_a]["lat"], graph["nodes"][city_a]["lon"]
        
        # Calculate straight-line distance to all other cities
        distances = []
        for city_b in node_names:
            if city_a != city_b:
                lat_b, lon_b = graph["nodes"][city_b]["lat"], graph["nodes"][city_b]["lon"]
                dist = math.hypot(lat_a - lat_b, lon_a - lon_b)
                distances.append((dist, city_b))
                
        # Sort to find the 3 geographically closest cities to guarantee a fully connected web
        distances.sort()
        closest_neighbors = [c[1] for c in distances[:3]] 
        
        for city_b in closest_neighbors:
            # Check if edge already exists to prevent duplicate API calls
            if city_b not in graph["edges"][city_a]:
                lat_b, lon_b = graph["nodes"][city_b]["lat"], graph["nodes"][city_b]["lon"]
                route_dist = get_route_distance(lat_a, lon_a, lat_b, lon_b)
                
                # Build undirected edges
                graph["edges"][city_a][city_b] = route_dist
                graph["edges"][city_b][city_a] = route_dist
                print(f"  Connected: {city_a} <-> {city_b} ({route_dist} miles)")
                time.sleep(0.5) # Respect OSRM rate limits

    with open("map_data.json", "w") as f:
        json.dump(graph, f, indent=4)
        
    print("\nGraph successfully built and saved to map_data.json!")

if __name__ == "__main__":
    build_graph()
