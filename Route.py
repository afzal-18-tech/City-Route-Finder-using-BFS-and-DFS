# City Route Finder using BFS and DFS
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

# Define the city graph (Adjacency List)
city_graph = {
    'Delhi': ['Jaipur', 'Agra'],
    'Jaipur': ['Delhi', 'Bhopal', 'Indore'],
    'Agra': ['Delhi', 'Kanpur'],
    'Bhopal': ['Jaipur', 'Patna'],
    'Indore': ['Jaipur', 'Surat'],
    'Kanpur': ['Agra', 'Lucknow'],
    'Patna': ['Bhopal', 'Hyderabad'],
    'Surat': ['Indore', 'Mumbai'],
    'Lucknow': ['Kanpur'],
    'Hyderabad': ['Patna', 'Mumbai'],
    'Mumbai': ['Surat', 'Hyderabad']
}

# BFS Algorithm
def bfs(start, goal):
    visited = set()
    queue = deque([[start]])
    while queue:
        path = queue.popleft()
        city = path[-1]
        if city == goal:
            return path
        if city not in visited:
            for neighbor in city_graph.get(city, []):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
            visited.add(city)
    return None

# DFS Algorithm
def dfs(start, goal, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = [start]
    visited.add(start)
    if start == goal:
        return path
    for neighbor in city_graph.get(start, []):
        if neighbor not in visited:
            new_path = dfs(neighbor, goal, visited, path + [neighbor])
            if new_path:
                return new_path
    return None

# Input
start_city = 'Kanpur'
goal_city = 'Mumbai'

# Find routes
bfs_path = bfs(start_city, goal_city)
dfs_path = dfs(start_city, goal_city)

# Print results
print("----- City Route Finder -----")
print(f"Start City: {start_city}")
print(f"Destination City: {goal_city}")
print("\nBFS Path (Shortest Route):", ' → '.join(bfs_path))
print("DFS Path (Deep Exploration):", ' → '.join(dfs_path))

# Graph Visualization
G = nx.Graph()

# Add edges
for city, connections in city_graph.items():
    for neighbor in connections:
        G.add_edge(city, neighbor)

# Graph layout
pos = nx.spring_layout(G, seed=42)

# Draw base graph
nx.draw(G, pos, with_labels=True, node_size=1200, node_color="blue", font_size=10, font_weight='bold')

# Highlight BFS path
bfs_edges = list(zip(bfs_path, bfs_path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=bfs_edges, edge_color="yellow", width=3, label="BFS Path")

# Highlight DFS path
dfs_edges = list(zip(dfs_path, dfs_path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=dfs_edges, edge_color="red", width=3, style='dashed', label="DFS Path")

# Add legend and title
plt.title("City Route Finder using BFS and DFS")
plt.legend()
plt.show()
