class PostSearch:
    def __init__(self, xml_file):
        """
        Initialize the PostSearch object by loading the XML file content as a string.
        """
        with open(xml_file, 'r', encoding='utf-8') as file:
            self.xml_content = file.read()

    def search_word(self, word):
        """
        Search for posts containing a specific word in the <body> of <post> (case-insensitive).
        """
        posts = []
        user_start = 0
        word_lower = word.lower()  # Convert the search word to lowercase for case-insensitive comparison

        # Iterate over <user> elements
        while True:
            user_start = self.xml_content.find("<user>", user_start)
            if user_start == -1:
                break
            user_end = self.xml_content.find("</user>", user_start)
            user_content = self.xml_content[user_start:user_end]

            # Iterate over <post> elements within the user
            post_start = 0
            while True:
                post_start = user_content.find("<post>", post_start)
                if post_start == -1:
                    break
                post_end = user_content.find("</post>", post_start)
                post_content = user_content[post_start:post_end]

                # Extract <body> and check for the word
                body_content = self._extract_tag_value(post_content, "body")
                if body_content and word_lower in body_content.lower():  # Case-insensitive comparison
                    posts.append(body_content.strip())
                post_start = post_end + len("</post>")
            user_start = user_end + len("</user>")
        return posts

    def search_topic(self, topic):
        """
        Search for posts where the given topic is mentioned in the <topic> tag (case-insensitive).
        """
        posts = []
        user_start = 0
        topic_lower = topic.lower()  # Convert the search topic to lowercase for case-insensitive comparison

        # Iterate over <user> elements
        while True:
            user_start = self.xml_content.find("<user>", user_start)
            if user_start == -1:
                break
            user_end = self.xml_content.find("</user>", user_start)
            user_content = self.xml_content[user_start:user_end]

            # Iterate over <post> elements within the user
            post_start = 0
            while True:
                post_start = user_content.find("<post>", post_start)
                if post_start == -1:
                    break
                post_end = user_content.find("</post>", post_start)
                post_content = user_content[post_start:post_end]

                # Check if the topic is mentioned
                topic_content = self._extract_tag_value(post_content, "topic")
                if topic_content and topic_content.lower() == topic_lower:  # Case-insensitive comparison
                    # Extract the body of the post
                    body_content = self._extract_tag_value(post_content, "body")
                    if body_content:
                        posts.append(body_content.strip())
                post_start = post_end + len("</post>")
            user_start = user_end + len("</user>")
        return posts


    def search_word_topic(self, word, topic):
        """
        Search for posts containing a specific word and having a specific topic.
        """
        word_posts = []
        topic_posts = []
        # Search for posts containing the word
        word_posts = self.search_word(word)

        # Search for posts with the specific topic
        topic_posts = self.search_topic(topic)

        # Find the intersection of both lists
        result_posts = [post for post in word_posts if post in topic_posts]

        return result_posts
    

    def _extract_tag_value(self, content, tag):
        """
        Extract the value of a given tag from the content.
        """
        start_tag = f"<{tag}>"
        end_tag = f"</{tag}>"
        start = content.find(start_tag)
        if start == -1:
            return None
        start += len(start_tag)
        end = content.find(end_tag, start)
        if end == -1:
            return None
        return content[start:end]



# Example Usage
# Ensure the XML file path is correct
xml_file_path = r"samples/test.xml"  # Use raw string or forward slashes

searcher = PostSearch(xml_file_path)

"""
# Search for posts containing a specific word (case-insensitive)
word = "EXercitation "
word_results = searcher.search_word(word)
print(f"Posts containing the word '{word}':")
for post_body in word_results:
    print(post_body)

# Search for posts with a specific topic (case-insensitive)
topic = "tOPiC1"
topic_results = searcher.search_topic(topic)
print(f"\nPosts with topic '{topic}':")
for post_body in topic_results:
    print(post_body)
"""