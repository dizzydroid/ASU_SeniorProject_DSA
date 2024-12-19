class PostSearch:
   
    def __init__(self, xml_file):  
        """
        Initialize the PostSearch object by loading the XML file content as a string.
        """
        with open(xml_file, 'r', encoding='utf-8') as file:
            self.xml_content = file.read()

    def search_word(self, word):
       
        posts = []
        start = 0
        while True:
            start = self.xml_content.find("<post", start)
            if start == -1:
                break
            end = self.xml_content.find("</post>", start)
            if end == -1:
                break
            post_content_start = self.xml_content.find(">", start) + 1

            post_content = self.xml_content[post_content_start:end].strip()
            if word in post_content:
                if ">" in post_content:
                    post_content = post_content.split(">", 1)[-1]
                posts.append(post_content)
            start = end + 7  # 7 is the length of "</post>"
        return posts

    def search_topic(self, topic):
        posts = []
        start = 0
        while True:
            start = self.xml_content.find("<post ", start)
            if start == -1:
                break
            topic_start = self.xml_content.find("topic=\"", start)
            if topic_start == -1 or topic_start > self.xml_content.find(">", start):
                start = self.xml_content.find("</post>", start) + 7
                continue
            topic_end = self.xml_content.find("\"", topic_start + 7)
            post_topic = self.xml_content[topic_start + 7:topic_end]
            if post_topic == topic:
                post_content_start = self.xml_content.find(">", start) + 1
                end = self.xml_content.find("</post>", start)
                if end == -1:
                    break
                post_content = self.xml_content[post_content_start:end].strip()
                posts.append(post_content)
            start = self.xml_content.find("</post>", start) + 7
        return posts
"""

# Example Usage
# Initialize the class with an XML file
searcher = PostSearch("samples\post_search_sample.xml")  # Ensure the path to your XML file is correct

# Search for posts containing a specific word
word_posts = searcher.search_word("shaping")
print("Posts containing :", word_posts)

# Search for posts with a specific topic
topic_posts = searcher.search_topic("technology")
print("Posts with topic :", topic_posts)
"""