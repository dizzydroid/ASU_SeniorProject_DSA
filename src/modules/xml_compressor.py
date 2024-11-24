from collections import Counter
import json

import re

class XMLCompressor:
    def __init__(self):
        self.compression_map = {}  # Maps patterns to tokens
        self.decompression_map = {}  # Maps tokens back to patterns

    def compress(self, content):
        """
        Compresses XML content by replacing repetitive patterns with short tokens.
        """
        # Identify repeating tags or words
        patterns = re.findall(r"<(/?)(\w+)>", content)
        tag_counts = {}
        for _, tag in patterns:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # Sort tags by frequency
        sorted_tags = sorted(tag_counts.items(), key=lambda x: -x[1])

        # Assign short tokens to frequent tags
        for idx, (tag, _) in enumerate(sorted_tags):
            token = f"@{idx}"  # Create a short token
            self.compression_map[tag] = token
            self.decompression_map[token] = tag

        # Replace tags in the content with tokens
        compressed_content = content
        for tag, token in self.compression_map.items():
            compressed_content = re.sub(f"<{tag}>", f"<{token}>", compressed_content)
            compressed_content = re.sub(f"</{tag}>", f"</{token}>", compressed_content)

        return compressed_content

input_xml = "/home/seifelwarwary/_colcode/ASU_SeniorProject_DSA/samples/large_sample.xml"  # Path to your XML file
output_json = "/home/seifelwarwary/_colcode/ASU_SeniorProject_DSA/samples/compressed_data.json"  # Path to save the converted JSON file

xml_data = """
<users>
    <user id="1">
        <name>John Doe</name>
        <posts>
            <post>First post</post>
            <post>Second post</post>
        </posts>
        <followers>
            <follower id="2" />
        </followers>
    </user>
</users>
"""

import re

def parse_xml(xml_string):
    """
    Parses XML string into a dictionary representation.
    """
    # Define a helper function to process individual XML tags
    def process_element(tag_str):
        # Strip leading/trailing spaces
        tag_str = tag_str.strip()
        
        # Extract tag name and attributes
        tag_name = re.match(r"([a-zA-Z0-9]+)", tag_str).group(1)
        attributes = {}
        attr_match = re.findall(r'(\w+)="([^"]+)"', tag_str)
        for attr in attr_match:
            attributes[attr[0]] = attr[1]
        
        return tag_name, attributes
    
    # Define a helper function to recursively parse elements
    def parse_element(xml_str):
        tag_stack = []
        root = {}
        current_tag = None
        children = []
        content = ''
        
        # Split the XML string into tags and text
        tag_pattern = r"</?([a-zA-Z0-9]+(?:\s+[^>]*?)?)>|([^<]+)"
        parts = re.findall(tag_pattern, xml_str)
        
        for part in parts:
            tag, text = part
            
            if tag:  # It's a tag
                if tag.startswith('</'):  # Closing tag
                    tag_name = tag[2:-1].strip()
                    if current_tag:
                        if children:
                            root[current_tag] = {'children': children}
                        else:
                            root[current_tag] = {'content': content.strip()}
                    tag_stack.pop()  # Remove the last tag from the stack
                    current_tag = tag_stack[-1] if tag_stack else None
                    children = []
                else:  # Opening tag
                    tag_name, attributes = process_element(tag)
                    tag_stack.append(tag_name)
                    current_tag = tag_name
                    children = []
                    if current_tag not in root:
                        root[current_tag] = {'attributes': attributes, 'children': children}
                content = ''
            elif text.strip():  # Text content
                content += text.strip()
        
        return root
    
    # Parse the XML string into a dictionary
    return parse_element(xml_string.strip())

xml_data = """
<users>
    <user id="1">
        <name>John Doe</name>
        <posts>
            <post>First post</post>
            <post>Second post</post>
        </posts>
        <followers>
            <follower id="2" />
        </followers>
    </user>
</users>
"""
print(parse_xml(xml_data))