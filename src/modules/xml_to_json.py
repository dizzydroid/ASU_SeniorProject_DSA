import json
import xml.etree.ElementTree as ET

class XMLToJSONConverter:
    def __init__(self, input_file):
        self.input_file = input_file

    def convert(self, output_path):
        # Parse the input XML file into an ElementTree object
        tree = ET.parse(self.input_file)
        root = tree.getroot()

        # Convert the root element of the XML tree to a JSON-compatible dictionary
        json_data = self.convert_element(root)

        # Write the JSON data to the specified output file
        with open(output_path, 'w') as f:
            json.dump(json_data, f, indent=4)
        
        # Inform the user that the conversion was successful and provide the output file path
        print(f'Successfully converted XML to JSON. Output file saved at: {output_path}')

    def convert_element(self, element):
        json_data = {}

        # Add the element's attributes to the dictionary
        for attr_name, attr_value in element.attrib.items():
            json_data[attr_name] = attr_value

        # Add the element's text content to the dictionary, if it exists
        if element.text and element.text.strip():
            json_data['text'] = element.text.strip()

        # Recursively convert the element's children and add them to the dictionary
        for child in element:
            child_data = self.convert_element(child)
            if child.tag not in json_data:
                json_data[child.tag] = []
            json_data[child.tag].append(child_data)

        return json_data