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
        default_node_color="lightblue",
        font_size=10,
        edge_color="black",
        title="Directed Network Graph",
        most_active_users=None,
        most_influential_users=None,
    ):
        """
        Generate a visual representation of the directed graph with enhanced arrows and highlighted users.

        Args:
            most_active_users (list): List of user IDs for most active users
            most_influential_users (list): List of user IDs for most influential users
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

        # Create color map for nodes
        node_colors = []
        for node in G.nodes():
            if most_active_users and node in most_active_users:
                if most_influential_users and node in most_influential_users:
                    node_colors.append("purple")  # Both active and influential
                else:
                    node_colors.append("red")  # Only active
            elif most_influential_users and node in most_influential_users:
                node_colors.append("green")  # Only influential
            else:
                node_colors.append(default_node_color)

        # Draw the network - nodes first
        nx.draw_networkx_nodes(
            G,
            pos,
            node_size=node_size,
            node_color=node_colors,
            edgecolors="black",
            linewidths=2,
        )

        # Draw edges with enhanced arrows
        edges = nx.draw_networkx_edges(
            G,
            pos,
            edge_color=edge_color,
            width=2,
            arrows=True,
            arrowsize=40,
            arrowstyle="->",
            connectionstyle="arc3,rad=0.2",
            min_source_margin=35,
            min_target_margin=35,
        )

        # Add labels with white background for better visibility
        labels = {user.id: f"{user.name}\n(ID: {user.id})" for user in self.graph.users}
        label_boxes = nx.draw_networkx_labels(
            G,
            pos,
            labels,
            font_size=font_size,
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.7, pad=5),
        )

        # Add legend
        legend_elements = []
        if most_active_users:
            legend_elements.append(
                plt.Line2D(
                    [0],
                    [0],
                    marker="o",
                    color="w",
                    markerfacecolor="red",
                    markersize=15,
                    label="Most Active",
                )
            )
        if most_influential_users:
            legend_elements.append(
                plt.Line2D(
                    [0],
                    [0],
                    marker="o",
                    color="w",
                    markerfacecolor="green",
                    markersize=15,
                    label="Most Influential",
                )
            )
        if most_active_users and most_influential_users:
            legend_elements.append(
                plt.Line2D(
                    [0],
                    [0],
                    marker="o",
                    color="w",
                    markerfacecolor="purple",
                    markersize=15,
                    label="Both Active & Influential",
                )
            )
        if legend_elements:
            plt.legend(handles=legend_elements, loc="upper left", bbox_to_anchor=(1, 1))

        # Add title
        plt.title(title, fontsize=16, pad=20)

        # Remove axis
        plt.axis("off")

        # Add more space around the plot
        plt.margins(0.2)
        plt.tight_layout()
        plt.savefig(
            "graph.png" if save_path is None else save_path, bbox_inches="tight"
        )  # Added bbox_inches to prevent legend cutoff
        plt.close()
