import json
import re
import traceback

class XMLCustomParser:
    """Custom XML parsing helper class"""
    @staticmethod
    def tokenize(xml_string):
        """
        Tokenize XML string into meaningful tokens
        
        Args:
            xml_string (str): Raw XML content
        
        Returns:
            list: Cleaned and tokenized XML elements
        """
        # Remove XML declaration, comments, and normalize whitespace
        xml_string = re.sub(r'<\?xml.*?\?>', '', xml_string)
        xml_string = re.sub(r'<!--.*?-->', '', xml_string, flags=re.DOTALL)
        
        # Sophisticated tokenization with improved regex
        tokens = re.findall(r'<[^>]+>|[^<\s][^<]*', xml_string)
        
        # Clean and filter tokens
        tokens = [token.strip() for token in tokens if token.strip()]
        return tokens

    @staticmethod
    def parse_tag(tag):
        """
        Parse XML tag to extract tag name and attributes
        
        Args:
            tag (str): XML tag string
        
        Returns:
            tuple: (tag_name, attributes_dict)
        """
        # Remove angle brackets and handle self-closing tags
        tag = tag.strip('<>/')
        
        # Split tag into parts
        parts = tag.split()
        if not parts:
            return '', {}
        
        # First part is the tag name
        tag_name = parts[0]
        
        # Parse attributes
        attributes = {}
        for attr in parts[1:]:
            # More flexible attribute parsing
            attr_match = re.match(r'([\w-]+)=(["\'])(.*?)\2', attr)
            if attr_match:
                key, _, value = attr_match.groups()
                attributes[key] = value
        
        return tag_name, attributes

class CustomTreeNode:
    """Custom tree node representation"""
    def __init__(self, tag=None, text=None, attributes=None):
        """
        Initialize a tree node
        
        Args:
            tag (str, optional): XML tag name
            text (str, optional): Text content
            attributes (dict, optional): Node attributes
        """
        self.tag = tag
        self.text = text.strip() if text and text.strip() else None
        self.attributes = attributes or {}
        self.children = []
    
    def add_child(self, child):
        """
        Add a child node
        
        Args:
            child (CustomTreeNode): Child node to add
        """
        self.children.append(child)

class XMLToJSONConverter:
    def __init__(self, input_file):
        """
        Initialize the converter with input file
        
        Args:
            input_file (str): Path to the input XML file
        """
        self.input_file = input_file
        self._parser = XMLCustomParser()
        self._debug_info = {
            'current_context': [],
            'tokens': []
        }

    def convert_element(self, node):
        """
        Convert a node to JSON-compatible dictionary
        Args:
            node (CustomTreeNode): Node to convert
        Returns:
            dict: JSON-compatible representation
        """
        # If the node has no attributes or children, and only text, return the text directly
        if not node.attributes and not node.children and node.text:
            return node.text
        
        # Start with attributes
        json_data = dict(node.attributes)
        
        # Add text if exists and there are children (handle inline text)
        if node.text and node.children:
            json_data['text'] = node.text
        elif node.text:  # No children, treat text as direct value
            return node.text
        
        # Process children
        for child in node.children:
            if child.tag not in json_data:
                json_data[child.tag] = []
            json_data[child.tag].append(self.convert_element(child))
        
        # Collapse lists with a single item to simplify structure
        for key, value in json_data.items():
            if isinstance(value, list) and len(value) == 1:
                json_data[key] = value[0]
        
        return json_data


    def _build_tree(self, tokens):
        """
        Build a tree from XML tokens
        
        Args:
            tokens (list): Tokenized XML elements
        
        Returns:
            CustomTreeNode: Root of the parsed XML tree
        """
        # Store tokens for debug purposes
        self._debug_info['tokens'] = tokens.copy()
        
        if not tokens:
            raise ValueError("Empty XML content")
        
        # Stack to track nested elements
        stack = []
        root = None
        
        try:
            while tokens:
                token = tokens.pop(0)
                # Debugging: track current context
                self._debug_info['current_context'] = [node.tag for node in stack]
                
                # Opening tag (not closing, not self-closing)
                if token.startswith('<') and not token.startswith('</') and not token.endswith('/>'):
                    # Parse tag
                    tag_name, attributes = self._parser.parse_tag(token)
                    
                    # Create new node
                    new_node = CustomTreeNode(tag=tag_name, attributes=attributes)
                    
                    # Add to parent if exists
                    if stack:
                        stack[-1].add_child(new_node)
                    
                    # Push to stack
                    stack.append(new_node)
                    
                    # Set root if not set
                    if not root:
                        root = new_node
                
                # Closing tag
                elif token.startswith('</'):
                    # Validate closing tag
                    closing_tag = token.strip('</>')
                    
                    if not stack:
                        raise ValueError(f"Unexpected closing tag: {closing_tag}")
                    
                    if stack[-1].tag != closing_tag:
                        # Provide detailed context for the mismatch
                        context = ' > '.join(node.tag for node in stack)
                        raise ValueError(
                            f"Mismatched closing tag: Expected </>{stack[-1].tag}, "
                            f"found </{closing_tag}>. Context: {context}"
                        )
                    
                    # Pop from stack
                    stack.pop()
                
                # Self-closing tag
                elif token.startswith('<') and token.endswith('/>'):
                    # Parse self-closing tag
                    tag_name, attributes = self._parser.parse_tag(token)
                    
                    # Create and add node
                    self_closing_node = CustomTreeNode(tag=tag_name, attributes=attributes)
                    
                    if stack:
                        stack[-1].add_child(self_closing_node)
                    elif not root:
                        root = self_closing_node
                
                # Text content
                else:
                    # Add text to current top of stack
                    if stack:
                        current_node = stack[-1]
                        if not current_node.text:
                            current_node.text = token
                        else:
                            current_node.text += ' ' + token
        
        except Exception as e:
            # Enhance error with debug information
            error_details = (
                f"Error Details:\n"
                f"Tokens Remaining: {tokens}\n"
                f"Current Context: {self._debug_info['current_context']}\n"
                f"Full Token List: {self._debug_info['tokens']}"
            )
            raise ValueError(f"{str(e)}\n{error_details}") from e
        
        # Ensure all tags are closed
        if stack:
            context = ' > '.join(node.tag for node in stack)
            raise ValueError(f"Not all tags were closed. Unclosed tags: {context}")
        
        return root

    def convert(self, output_path):
        """
        Convert XML file to JSON
        
        Args:
            output_path (str): Path to save the output JSON file
        """
        try:
            # Read input file
            with open(self.input_file, 'r', encoding='utf-8') as f:
                xml_content = f.read()
            
            # Tokenize XML
            tokens = self._parser.tokenize(xml_content)

            
            # Build tree
            root = self._build_tree(tokens)

            # Convert to JSON with root tag as key
            json_data = {root.tag: self.convert_element(root)}

            # Write JSON
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=4)
            
            print(f'Successfully converted XML to JSON. Output file saved at: {output_path}')
        
        except (IOError, ValueError) as e:
            # Enhanced error reporting
            print(f"Error converting XML to JSON: {str(e)}")
            raise

# Example usage
# if __name__ == '__main__':
#     try:
#         converter = XMLToJSONConverter(r'path_to_file')
#         converter.convert(r'path_to_file')
#     except Exception as e:
#         # User-friendly error message
#         print("Oops! Something went wrong during the XML to JSON conversion. Please check your XML file for errors.")
        
#         # Log detailed error information
#         with open('error_log.txt', 'w') as error_log:
#             error_log.write(f"Error Details:\n{traceback.format_exc()}\n")
