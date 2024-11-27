import xml.etree.ElementTree as ET

class XMLMinifier:
    def __init__(self, file_path):
        self.file_path = file_path

    def remove_comments(self, root):
        """Remove comments from the XML root."""
        # Iterate over each element in the XML tree
        for elem in root.findall('.//*'):
            comments_to_remove = [
                c for c in list(elem) if isinstance(c, ET.Element) and c.tag == ET.Comment
            ]
            # Remove collected comments
            for comment in comments_to_remove:
                elem.remove(comment)

    def clean_element(self, element):
        """Recursively clean up spaces and newlines in the XML elements."""
        if element.text:
            element.text = element.text.strip()
        if element.tail:
            element.tail = element.tail.strip()
        for child in element:
            self.clean_element(child)

    def minify(self, output_path):
        """Minify the XML by removing comments and cleaning spaces."""
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()

            # Remove comments and clean XML
            self.remove_comments(root)
            self.clean_element(root)

            # Write the cleaned XML to the output file
            with open(output_path, 'wb') as f:
                f.write(ET.tostring(root, encoding='utf-8'))

            print(f"Minified XML written to {output_path}")

        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

