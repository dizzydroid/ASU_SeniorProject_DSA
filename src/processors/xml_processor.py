from src.modules.xml_parser import XMLParser
from src.modules.xml_formatter import XMLFormatter
from src.modules.xml_minifier import XMLMinifier
from src.modules.xml_compressor import XMLCompressor
from src.modules.xml_decompressor import XMLDecompressor

class XMLProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, "r") as file:
            self.content = file.read()
        self.parser = XMLParser(file_path)
        self.formatter = XMLFormatter()
        self.minifier = XMLMinifier()
        self.compressor = XMLCompressor()
        self.decompressor = XMLDecompressor()

    def prettify(self, inplace=False):
        self.content = self.formatter.prettify(self.content)
        if inplace:
            self._write_to_file(self.file_path)
        return self

    def minify(self, inplace=False):
        self.content = self.minifier.minify(self.content)
        if inplace:
            self._write_to_file(self.file_path)
        return self

    def compress(self, inplace=False):
        self.content = self.compressor.compress(self.content)
        if inplace:
            self._write_to_file(self.file_path)
        return self

    def decompress(self, inplace=False):
        self.content = self.decompressor.decompress(self.content)
        if inplace:
            self._write_to_file(self.file_path)
        return self

    def save(self, output_path=None):
        if not output_path:
            output_path = self.file_path
        self._write_to_file(output_path)

    def _write_to_file(self, path):
        with open(path, "w") as file:
            file.write(self.content)
        print(f"File saved to {path}")
