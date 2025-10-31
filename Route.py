# City Route Finder using BFS and DFS (Tkinter GUI)
from tkinter import *
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# --- Define City Graph ---
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

# --- BFS Algorithm ---
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

# --- DFS Algorithm ---
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

# --- Graph Visualization ---
def visualize_path(path, color):
    G = nx.Graph()
    for city, connections in city_graph.items():
        for neighbor in connections:
            G.add_edge(city, neighbor)
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8,6))
    nx.draw(G, pos, with_labels=True, node_size=1200, node_color="lightblue", font_size=10, font_weight='bold')
    if path:
        edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=color, width=3)
    plt.title("City Route Visualization")
    plt.show()

# --- GUI Implementation ---
def find_route():
    start = start_city.get()
    end = dest_city.get()
    algo = algorithm.get()

    if start == end:
        messagebox.showwarning("Warning", "Start and Destination cannot be the same!")
        return

    if algo == "Breadth First Search (BFS)":
        path = bfs(start, end)
        color = "yellow"
    else:
        path = dfs(start, end)
        color = "red"

    if path:
        messagebox.showinfo("Route Found", f"Path: {' → '.join(path)}")
        visualize_path(path, color)
    else:
        messagebox.showerror("Error", "No route found between selected cities!")

# --- Create Window ---
root = Tk()
root.title("City Route Finder using BFS and DFS")
root.geometry("500x400")
root.configure(bg="#f2f2f2")

Label(root, text="CITY ROUTE FINDER", font=("Arial", 16, "bold"), bg="#f2f2f2").pack(pady=10)

Label(root, text="Select Starting City:", bg="#f2f2f2", font=("Arial", 11)).pack()
start_city = ttk.Combobox(root, values=list(city_graph.keys()), width=30)
start_city.pack(pady=5)

Label(root, text="Select Destination City:", bg="#f2f2f2", font=("Arial", 11)).pack()
dest_city = ttk.Combobox(root, values=list(city_graph.keys()), width=30)
dest_city.pack(pady=5)

Label(root, text="Choose Algorithm:", bg="#f2f2f2", font=("Arial", 11)).pack()
algorithm = ttk.Combobox(root, values=["Breadth First Search (BFS)", "Depth First Search (DFS)"], width=30)
algorithm.pack(pady=5)

Button(root, text="Find Route", command=find_route, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), width=20).pack(pady=15)
Button(root, text="Exit", command=root.destroy, bg="#E74C3C", fg="white", font=("Arial", 11, "bold"), width=20).pack(pady=5)

root.mainloop()
