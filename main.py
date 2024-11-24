from src.processors.xml_processor import XMLProcessor

def main():
    processor = XMLProcessor("sample_files/sample.xml")
    processor.prettify().minify().compress().save("sample_files/output.xml")
    print("Operations completed successfully!")

if __name__ == "__main__":
    main()
