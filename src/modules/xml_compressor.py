import re
class XMLCompressor:
    def __init__(self, input_path):
        self.input_path = input_path

    def compress(self, output_path):
        with open(self.input_path, 'r', encoding='utf-8') as file:
            data = file.read()

        compressed_data = re.sub(r'</[^>]+>', '</>', data)

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(compressed_data)

# Usage
# compressor = XMLCompressor('../../samples/large_sample.xml')
# compressor.compress('../../samples/output.compressed')

