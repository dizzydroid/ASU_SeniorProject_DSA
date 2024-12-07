class XMLMinifier:
    def __init__(self, file_path):
        self.file_path = file_path

    def remove_comments(self, xml_content):
        """
        Removes all comments from the XML content.
        XML comments are of the format <!-- comment -->
        """
        result = []
        inside_comment = False

        i = 0
        while i < len(xml_content):
            if xml_content[i:i+4] == "<!--":
                inside_comment = True
                i += 4
            elif inside_comment and xml_content[i:i+3] == "-->":
                inside_comment = False
                i += 3
            elif not inside_comment:
                result.append(xml_content[i])
                i += 1
            else:
                i += 1

        return ''.join(result)

    def clean_whitespace(self, xml_content):
        """
        Removes unnecessary whitespace (e.g., leading/trailing spaces, newlines).
        Retains meaningful spaces within text nodes.
        """
        result = []
        inside_tag = False
        buffer = []

        i = 0
        while i < len(xml_content):
            char = xml_content[i]

            if char == "<":
                # If there's accumulated text, trim and add it to result
                if buffer:
                    trimmed_text = ''.join(buffer).strip()
                    if trimmed_text:
                        result.append(trimmed_text)
                    buffer = []
                inside_tag = True
                result.append(char)
            elif char == ">":
                inside_tag = False
                result.append(char)
            elif inside_tag:
                result.append(char)
            else:
                # Accumulate text content outside of tags
                buffer.append(char)

            i += 1

        # Add any remaining text outside tags
        if buffer:
            trimmed_text = ''.join(buffer).strip()
            if trimmed_text:
                result.append(trimmed_text)

        return ''.join(result)

    def minify(self, output_path):
        """
        Minifies the XML file by removing comments and cleaning unnecessary whitespace.
        """
        try:
            # Read the XML content from the file
            with open(self.file_path, 'r', encoding='utf-8') as file:
                xml_content = file.read()

            # Remove comments and clean whitespace
            xml_content = self.remove_comments(xml_content)
            xml_content = self.clean_whitespace(xml_content)

            # Write the cleaned XML content to the output file
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(xml_content)

            print(f"Minified XML written to {output_path}")

        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found.")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

#test
minifier = XMLMinifier("samples\commented_sample.xml")
minifier.minify("samples/output.xml")
