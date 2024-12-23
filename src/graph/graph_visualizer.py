import networkx as nx
import matplotlib.pyplot as plt

class GraphVisualizer:
    def __init__(self, graph_data):
        """
        Initialize the visualizer with graph data.
        :param graph_data: A networkx graph object.
        """
        self.graph = graph_data

    def visualize(self, highlight_node=None, save_path=None):
        """
        Visualize the graph.
        :param highlight_node: Optional node to highlight.
        :param save_path: Optional path to save the visualization as an image.
        """
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(self.graph)

        # Draw the graph
        nx.draw(
            self.graph, pos, with_labels=True, node_size=700, node_color="lightblue", edge_color="gray"
        )

        # Highlight specific node if provided
        if highlight_node:
            nx.draw_networkx_nodes(
                self.graph, pos, nodelist=[highlight_node], node_color="orange", node_size=800
            )

        plt.title("User Graph Visualization")
        if save_path:
            plt.savefig(save_path)
        plt.show()
