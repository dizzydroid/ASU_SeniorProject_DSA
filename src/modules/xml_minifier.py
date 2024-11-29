import xml.etree.ElementTree as ET

class XMLMinifier:
    def __init__(self, file_path):
        self.file_path = file_path

    # def remove_comments(self, element):
    # """Recursively remove comments from the XML elements."""
    # for child in list(element):
    #     if isinstance(child, ET.Comment):
    #         element.remove(child)
    #     else:
    #         self.remove_comments(child)

    def remove_comments(self, element):
        """Recursively remove comments from the XML elements.
        This function works by checking the tag of each child element.
        If the tag is a comment, the element is removed. Otherwise,
        the function recursively processes the child elements.
        """
        for child in list(element):
            if isinstance(child, ET.Element) and isinstance(child.tag, str) and child.tag.startswith("<!--"):
                element.remove(child)
            else:
                self.remove_comments(child)

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
            print(f"Parsing XML file: {self.file_path}")
            tree = ET.parse(self.file_path)
            root = tree.getroot()

            # Remove comments and clean XML
            print("Removing comments and cleaning XML elements")
            self.remove_comments(root)
            self.clean_element(root)

            # Write the cleaned XML to the output file
            with open(output_path, 'wb') as f:
                f.write(ET.tostring(root, encoding='utf-8'))

            print(f"Minified XML written to {output_path}")

        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise