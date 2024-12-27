import networkx as nx
import matplotlib.pyplot as plt
from src.graph.graph_representation import GraphRepresentation


class GraphVisualizer:
    def __init__(self, graph: GraphRepresentation):
        self.graph = graph

    def visualize(
        self,
        save_path="output.png",
        figsize=(12, 12),
        node_size=2000,
        node_color="lightblue",
        font_size=10,
        edge_color="black",
        title="Directed Network Graph",
    ):
        """
        Generate a visual representation of the directed graph with enhanced arrows.
        """
        # Create a directed networkx graph
        G = nx.DiGraph()

        # Add nodes (users)
        for user in self.graph.users:
            G.add_node(user.id, name=user.name)

        # Add directed edges from adjacency list
        for user_id, connections in self.graph.adjacency_list.items():
            for connected_id in connections:
                G.add_edge(user_id, connected_id)

        # Create the figure with high DPI for better quality
        plt.figure(figsize=figsize, dpi=100)

        # Use spring layout with more space between nodes
        pos = nx.spring_layout(G, k=2.5, iterations=50)

        # Draw the network - nodes first
        nx.draw_networkx_nodes(
            G,
            pos,
            node_size=node_size,
            node_color=node_color,
            edgecolors="black",  # Add black border to nodes
            linewidths=2,
        )  # Node border width

        # Draw edges with enhanced arrows
        edges = nx.draw_networkx_edges(
            G,
            pos,
            edge_color=edge_color,
            width=2,
            arrows=True,
            arrowsize=40,  # Larger arrows
            arrowstyle="->",  # Simple arrow style
            connectionstyle="arc3,rad=0.2",  # Curved edges
            min_source_margin=35,  # Space between arrow and source node
            min_target_margin=35,
        )  # Space between arrow and target node

        # Add labels with white background for better visibility
        labels = {user.id: f"{user.name}\n(ID: {user.id})" for user in self.graph.users}
        label_boxes = nx.draw_networkx_labels(
            G,
            pos,
            labels,
            font_size=font_size,
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.7, pad=5),
        )

        # Add title
        plt.title(title, fontsize=16, pad=20)

        # Remove axis
        plt.axis("off")

        # Add more space around the plot
        plt.margins(0.2)
        plt.tight_layout()
        plt.savefig("graph.png" if save_path is None else save_path)
        plt.close()
