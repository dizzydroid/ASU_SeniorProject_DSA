import networkx as nx
class Post:
    def __init__(self, body, topics):
        self.body = body
        self.topics: list[str] = topics  # list of topics (strings)

    def __repr__(self):
        return f"Post(body={self.body}, topics={self.topics})"


class User:
    def __init__(self, user_id: int, name: str):
        self.id: int = user_id
        self.name: str = name
        self.followers: list[int] = []  # list of follower ids (integers)
        self.posts: list[Post] = []  # list of Post objects

    def add_follower(self, follower_id: int):
        self.followers.append(follower_id)

    def add_post(self, post: Post):
        self.posts.append(post)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, followers={self.followers}, posts={self.posts})"


class GraphRepresentation:
    """
    Graph Respresentation Class

    Attributes
    ----------
    users: List[User]
        List of all user nodes
    edges: List[Tuple[int, int]]
        List of all edges (userid1 -> userid2) userid2 is a follower of userid1
    adjacency_list: Dictionary[int, List[int]]
        Dictionary with user id for keys, and user followers list for values

    Methods
    -------
    build_graph(xml_file)
        Return instance of graph representation for xml_file

        Usage:
            graph = GraphRepresentation.build_graph(xml_text)

    get_user(user_id)
        Return user object given the id

    user_exists(user_id)
        Return true if user with given id exists , false otherwise
    """

    def __init__(self, *, users=None, edges=None, adjacency_list=None):
        self.users: list[User] = users if users else []
        self.edges = edges if edges else []
        self.adjacency_list: dict[int, list[int]] = (
            adjacency_list if adjacency_list else {}
        )

        # Create the networkx graph
        self.graph = self._create_networkx_graph() #edited
        
    def _create_networkx_graph(self):  #edited
        """Creates and returns a networkx DiGraph from the current graph data"""
        G = nx.DiGraph()

        # Add nodes (users)
        for user in self.users:
            G.add_node(user.id)

        # Add edges from the edges list
        for edge in self.edges:
            G.add_edge(edge[0], edge[1])

        return G

    @classmethod
    def build_graph(cls, xml_file):
        """
        Parses XML data and builds the graph.
        Nodes represent users, edges represent follower relationships.

        Parameters
        ----------
        xml_file: xml
            file path to the xml file
        """

        users, adjacency_list, edges = cls.parse_xml_to_graph(xml_file)

        self = cls(users=users, adjacency_list=adjacency_list, edges=edges)
        return self

    def get_user(self, user_id):
        return next(filter(lambda user: user_id == user.id, self.users), None)

    def user_exists(self, user_id):
        return any(user.id == user_id for user in self.users)

    @staticmethod
    def parse_xml_to_graph(xml_file_path):
        # Split the text based on the user blocks
        with open(xml_file_path, "r") as xml_file:
            xml_text = xml_file.read()

        users_data = xml_text.split("<user>")[1:]

        users = []
        edges = []
        adjacency_list = {}

        # First, parse all users and create them (without assigning followers yet)
        for user_data in users_data:
            user: User = User(
                user_id=int(_get_value(user_data, "<id>", "</id>")),
                name=_get_value(user_data, "<name>", "</name>"),
            )
            adjacency_list[user.id] = []

            # Parse posts
            posts_data = _get_values(user_data, "<post>", "</post>")
            for post_data in posts_data:
                body = _get_value(post_data, "<body>", "</body>")
                topics = _get_values(post_data, "<topic>", "</topic>")
                post = Post(body=body, topics=topics)
                user.add_post(post)

            # Parse followers
            followers_data = _get_values(user_data, "<follower>", "</follower>")
            for follower_data in followers_data:
                follower_id = int(_get_value(follower_data, "<id>", "</id>"))
                user.add_follower(follower_id)
                adjacency_list[user.id].append(follower_id)
                edges.append((user.id, follower_id))

            # Add the user to the users list (without followers for now)
            users.append(user)

        return users, adjacency_list, edges


def _get_value(data, start_tag, end_tag):
    """Extracts a value from the XML data between two tags."""
    start_index = data.find(start_tag) + len(start_tag)
    end_index = data.find(end_tag)
    return data[start_index:end_index].strip()


def _get_values(data, start_tag, end_tag):
    """Extracts a list of values from the XML data between two tags."""
    values = []
    start_index = 0
    while start_index != -1:
        start_index = data.find(start_tag, start_index)
        if start_index == -1:
            break
        end_index = data.find(end_tag, start_index)
        values.append(data[start_index + len(start_tag) : end_index].strip())
        start_index = end_index
    return values


###### Testing ######
# graph = GraphRepresentation.build_graph(r"D:\College\7th Semester\Data Structures and Algorithms (CSE331s)\Project\ASU_SeniorProject_DSA\samples\test.xml")
# print(graph.users)
# print(graph.adjacency_list)
