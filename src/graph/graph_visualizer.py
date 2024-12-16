import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt

class GraphVisualizer:
    def __init__(self, graph):
        self.graph = graph

    def draw_graph(self, output_file):
        """
        Draws the graph and saves it as an image.
        """
        pos = nx.spring_layout(self.graph)
        labels = nx.get_edge_attributes(self.graph, 'label')

        plt.figure(figsize=(10, 8))
        nx.draw(self.graph, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        plt.title("XML Graph Representation")
        plt.savefig(output_file)
        plt.close()
