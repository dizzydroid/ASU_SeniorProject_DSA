import xml.etree.ElementTree as ET

class PostSearch:
    def __init__(self, xml_file):
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()

    def search_word(self, word):
        """
        Returns posts that contain the given word.
        """
        posts = [post.text for post in self.root.findall(".//post") if word in post.text]
        return posts

    def search_topic(self, topic):
        """
        Returns posts that mention the given topic.
        """
        posts = [post.text for post in self.root.findall(f".//post[@topic='{topic}']")]
        return posts
