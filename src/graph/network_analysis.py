from graph_representation import GraphRepresentation as Graph

class NetworkAnalysis:
    def __init__(self, graph: Graph):
        self.graph = graph.graph

    def get_most_active_user(self):
        """
        Returns the user with the highest degree (most connections).
        """
        return max(self.graph.adjacency_list, key=lambda user: len(self.graph.adjacency_list[user]))

    def get_most_influencer_user(self):
        """
        Returns the user with the highest influence (centrality metric).
        """
        return self.get_most_active_user()

    def get_mutual_users(self, user_ids):
        """
        Returns mutual friends among given users.
        """
        mutual = set(self.graph.adjacency_list[user_ids[0]])
        for user_id in user_ids[1:]:
            mutual &= set(self.graph.adjacency_list[user_id])
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
