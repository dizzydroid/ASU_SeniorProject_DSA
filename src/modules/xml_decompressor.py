import re
class XMLDecompressor:
    def __init__(self, input_path):
        self.input_path = input_path

    def decompress(self, output_path):
        with open(self.input_path, 'r', encoding='utf-8') as file:
            compressed_data = file.read()

        open_tags = []

        def record_open_tag(match):
            tag_name = match.group(1)
            open_tags.append(tag_name)
            return match.group(0)

        def replace_closing_tag(match):
            if open_tags:
                tag_name = open_tags.pop()
                return f'</{tag_name}>'
            return match.group(0)

        # Record all open tags
        compressed_data = re.sub(r'<([^/!\s>]+)[^>]*>', record_open_tag, compressed_data)
        # Replace </> with the correct closing tags
        decompressed_data = re.sub(r'</>', replace_closing_tag, compressed_data)

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(decompressed_data)

# Usage
#decompressor = XMLDecompressor('../../samples/output.compressed')
#decompressor.decompress('../../samples/decompressed_output.xml')
