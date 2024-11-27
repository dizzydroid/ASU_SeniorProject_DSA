from src.processors.xml_processor import XMLProcessor
from src.modules.xml_minifier import XMLMinifier 


def main():
    
    #processor = XMLProcessor("sample_files/sample.xml")
    #processor.prettify().minify().compress().save("sample_files/output.xml")
    #print("Operations completed successfully!")

    # Create an instance of XMLMinifier with the input file
    #processor = XMLProcessor("sample_files/sample.xml")
    processor = XMLMinifier("samples/sample.xml")
    
    # Perform the minify operation and save to the output file
    processor.minify("samples/output.xml")
    
    print("XML minification completed successfully!")

if __name__ == "__main__":
    main()