class XMLDecompressor:
    def __init__(self, input_path):
        self.input_path = input_path

    def extract_tag(self, line, start):
        # Extract tag from line
        tag = "" 
        for char in line[start:]:
            if char == ' ' or char == '>':
                break
            elif char == '<':
                continue
            elif char == '?' or char == '!':
                return -1
            tag += char
        return tag

    def decompress(self, output_path):
        with open(self.input_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            open_tags = []

            for i, line in enumerate(lines):
                for j, char in enumerate(line):
                    if char == '<':
                        tag = self.extract_tag(line, j)
                        
                        if tag == -1:
                            continue
                        # Add opening tag to stack
                        if tag[0] != '/':
                            open_tags.append(tag)
                        else:
                            # If closing tag with no opening tag
                            if not open_tags:
                                raise Exception(f"Missing opening tag for {tag[1:]}")
                            else:
                                # Replace closing tag with correct closing tag
                                tag_name = open_tags.pop()
                                lines[i] = lines[i][:j] + f'</{tag_name}>' + lines[i][j + len(tag) + 2:]
                                
        # Write decompressed data to output file
        with open(output_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)



# Usage
decompressor = XMLDecompressor(r'../samples/compressed.xml')
decompressor.decompress(r'../samples/decompressed.xml')
