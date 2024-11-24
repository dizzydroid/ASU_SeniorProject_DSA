import gzip
import shutil


class XMLDecompressor:
    def __init__(self, file_path):
        self.file_path = file_path

    def decompress(self, output_path):
        with gzip.open(self.file_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
