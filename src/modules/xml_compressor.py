import gzip
import shutil
class XMLCompressor:
    def __init__(self, input_path):
        self.input_path = input_path

    def compress(self, output_path):
        with open(self.input_path, 'rb') as f_in:
            with gzip.open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)



input_xml = "/home/seifelwarwary/_colcode/ASU_SeniorProject_DSA/samples/large_sample.xml"
output_gz = "/home/seifelwarwary/_colcode/ASU_SeniorProject_DSA/samples/output.gz"

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


