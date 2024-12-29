from src.graph.graph_representation import GraphRepresentation as Graph

class NetworkAnalysis:
    def __init__(self, graph_rep: Graph):
        self.graph = graph_rep

    def get_most_active_user(self):
        """
        Returns the user with the highest degree (most connections).
        """
        most_active_user = max(self.graph.connections, key=lambda x: len(self.graph.connections[x])) if self.graph.connections else None
        if most_active_user:
            max_val = len(self.graph.connections[most_active_user])
            most_active_users = [most_active_user]
            for user in self.graph.connections:
                if user != most_active_user and len(self.graph.connections[user]) == max_val:
                    most_active_users.append(user)
            return most_active_users
        return most_active_user

    def get_most_influencer_user(self):
        """
        Returns the user with the highest influence in the network (most followers).
        Uses a priority queue (heap) to efficiently find the user with most followers.
        
        Returns:
            int: User ID of the most influential user
        """
        most_followed = max(self.graph.adjacency_list, key=lambda x: len(self.graph.adjacency_list[x])) if self.graph.adjacency_list else None
        if most_followed:
            max_val = len(self.graph.adjacency_list[most_followed])
            most_followed_users = [most_followed]
            for user in self.graph.adjacency_list:
                if user != most_followed and len(self.graph.adjacency_list[user]) == max_val:
                    most_followed_users.append(user)
            return most_followed_users
        return most_followed

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
        # Verify user exists
        if not self.graph.has_node(user_id):
            return []

        suggestions = set()

        # Get direct followers of the user
        direct_followers = set(self.graph.adjacency_list[user_id])

        # For each direct follower
        for follower in direct_followers:
            # Get their followers
            followers_of_follower = set(self.graph.adjacency_list[follower])
            suggestions.update(followers_of_follower)

        # Excluding from suggestions:
        # 1. The user themselves
        suggestions.discard(user_id)

        # 2. Direct followers of the user
        suggestions.difference_update(direct_followers)

        # 3. Users where the target user is already in their follower list
        suggestions = {
            suggestion for suggestion in suggestions
            if user_id not in self.graph.adjacency_list[suggestion]
        }

        return list(suggestions)


## Test items
# graph = Graph.build_graph(r"path/to/xml/file")
# net_analysis = NetworkAnalysis(graph)
# print(net_analysis.get_most_active_user())
# print(net_analysis.get_most_influencer_user())