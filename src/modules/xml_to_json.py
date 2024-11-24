import json

class XMLToJSONConverter:
    def __init__(self, file_path):
        self.file_path = file_path

    def convert(self, output_path):
        # Dummy function: Convert XML to JSON
        dummy_json = {"message": "This is a dummy JSON output"}
        with open(output_path, "w") as file:
            json.dump(dummy_json, file)
        print(f"Converted {self.file_path} to JSON at {output_path}")
