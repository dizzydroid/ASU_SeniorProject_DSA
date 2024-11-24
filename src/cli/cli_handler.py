from src.processors.xml_processor import XMLProcessor

class CLIHandler:
    def run(self):
        processor = XMLProcessor("input.xml")
        # Example: Perform prettify and save
        processor.prettify().save("output.xml")
