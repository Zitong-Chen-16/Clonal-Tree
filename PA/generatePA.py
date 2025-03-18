import networkx as nx
import os

def generate_connected_pa_graphs(num_graphs, num_nodes, m_range, output_folder="pa_graph_data2"):
    os.makedirs(output_folder, exist_ok=True)  # Create output folder if it doesn't exist
    
    m_values = list(range(*m_range))[:num_graphs]  # Generate different m values for each graph

    with open(f"{output_folder}/para.txt", 'w') as outfile:
        for i in range(1, len(m_values)+1):
            outfile.write(f"{i} {m_values[i-1]}\n")

    for i, m in enumerate(m_values):
        while True:
            # Generate a PA graph with the specified parameters
            G = nx.barabasi_albert_graph(num_nodes, m)
            
            # Check if the graph is connected
            if nx.is_connected(G):
                # Save edge list to a file
                edge_file_path = os.path.join(output_folder, f"pa_{i+1}.txt")
                with open(edge_file_path, 'w') as edge_file:
                    for edge in G.edges():
                        edge_file.write(f"{edge[0]} {edge[1]}\n")
                
                print(f"Generated and saved connected PA graph {i+1} with m = {m}")
                break  # Exit loop once a connected graph is found
            else:
                print(f"Graph with m = {m} was not connected, regenerating...")

# Example usage:
num_graphs = 20
num_nodes = 1000
m_range = (25, 101, 5)  # Define a range for m values from 1 to 20

generate_connected_pa_graphs(num_graphs, num_nodes, m_range)
