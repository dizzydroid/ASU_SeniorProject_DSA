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

# Example usage
# Initialize the class with an XML file
searcher = PostSearch("samples\\post_search_sample.xml")

# Search for posts containing a specific word
word_posts = searcher.search_word("Technology")
print("Posts containing :", word_posts)
