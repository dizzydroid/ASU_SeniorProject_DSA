from graph.graph_representation import GraphRepresentation as Graph


class NetworkAnalysis:
    def __init__(self, graph_rep: Graph):
        self.graph_rep = graph_rep
        self.graph = graph_rep.graph

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
        # Verify user exists
        if not self.graph.has_node(user_id):
            return []

        # Get current friends
        current_friends = set(self.graph.successors(user_id))

        # Get all users from graph
        all_users = set(self.graph.nodes())

        suggestion_scores = {}

        for potential_friend in all_users:
            # Skip if it's the user themselves or already a friend
            if potential_friend == user_id or potential_friend in current_friends:
                continue

            score = 0

            # Number of mutual friends
            mutual_friends = self.get_mutual_users([user_id, potential_friend])
            score += len(mutual_friends)

            if score > 0:
                suggestion_scores[potential_friend] = score

        # Sort by score and return user IDs
        sorted_suggestions = sorted(
            suggestion_scores.items(),
            key=lambda x: (-x[1], x[0])
        )

        return [user_id for user_id, _ in sorted_suggestions]
