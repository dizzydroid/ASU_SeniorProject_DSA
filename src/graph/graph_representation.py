import xml.etree.ElementTree as ET
import networkx as nx

class GraphRepresentation:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.graph = nx.DiGraph()  # Directed graph for user-post relationships

    def build_graph(self):
        """
        Parses XML data and builds the graph.
        Nodes represent users/posts, edges represent follower relationships.
        """
        tree = ET.parse(self.xml_file)
        root = tree.getroot()

        def add_edges(element, parent_id):
            """
            Recursively add nodes and edges to the graph.
            """
            for idx, child in enumerate(element):
                child_id = f"{parent_id}-{child.tag}-{idx}"
                self.graph.add_edge(parent_id, child_id, label=child.tag)
                add_edges(child, child_id)

        root_id = root.tag
        self.graph.add_node(root_id)
        add_edges(root, root_id)

    def get_graph(self):
        """
        Returns the graph object after building it.
        """
        if not self.graph.nodes:
            self.build_graph()
        return self.graph
