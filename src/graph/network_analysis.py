from graph_representation import GraphRepresentation as Graph
import networkx as nx
class NetworkAnalysis:
    def __init__(self, graph: Graph):
        self.graph : nx.DiGraph = graph.graph

    def get_most_active_user(self):
        """
        Returns the user with the highest degree (most connections).
        """
        return max(self.graph.adjacency_list, key=lambda user: len(self.graph.adjacency_list[user]))

    def get_most_influencer_user(self):
        """
        Returns the user with the highest influence in the network (most followers).
        Uses a priority queue (heap) to efficiently find the user with most followers.
        
        Returns:
            str: User ID of the most influential user
        """
        # Create a list to store (-follower_count, user_id) tuples
        # Using negative count for max heap since heapq implements min heap
        influence_heap = []
        
        # Count followers for each user
        for user in self.graph.nodes():
            follower_count = len(list(self.graph.predecessors(user)))
            # Push negative count for max heap behavior
            heapq.heappush(influence_heap, (-follower_count, user))
        
        # Get the user with the highest number of followers
        return influence_heap[0][1] if influence_heap else None

    def get_mutual_users(self, user_ids: list):
        """
        Returns mutual friends among given users.
        """
        if not user_ids:
            return []
        mutual = set(self.graph.successors(user_ids[0]))
        for user_id in user_ids[1:]:
            mutual &= set(self.graph.successors(user_id))

        return list(mutual)

    def get_suggested_users(self, user_id):
        """
        Returns user suggestions based on mutual friends.
        """
        suggestions = {}
        for friend in self.graph.adjacency_list[user_id]:
            for second_degree_friend in self.graph.adjacency_list[friend]:
                if second_degree_friend != user_id and second_degree_friend not in self.graph.adjacency_list[user_id]:
                    suggestions[second_degree_friend] = suggestions.get(second_degree_friend, 0) + 1
        return sorted(suggestions.keys(), key=lambda x: suggestions[x], reverse=True)
