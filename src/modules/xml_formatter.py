class XMLFormatter:
    def __init__(self, file_path: str):
        self.file_path: str = file_path

    def prettify(self, output_path: str, count: int = 4) -> None | str:
        """
        This function takes an input file and an output file and pretty prints the xml file.
        The count parameter is optional and is used to specify the number of spaces to use for indentation.
        It returns None if the file is successfully written to the output file.
        If the input file is not found, it returns a string indicating the file is not found.
        """
        try:
            with open(self.file_path, "r") as f:
                xml_file = f.read()
        except FileNotFoundError:
            return f"{self.file_path} is not Found"
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
        lines = (
            xml_file.replace(" ", "")
            .replace("\n", "")
            .replace("<", "\n<")
            .replace(">", ">\n")
            .split("\n")
        )

        indent = 0
        indent_str = " " * count
        pretty_lines = []
        for line in lines:
            if line == "":
                continue
            elif line.startswith("</"):
                indent -= 1

            pretty_lines.append(indent_str * indent + line)
            if line.startswith("<") and not line.startswith("</"):
                indent += 1

        pretty_xml = "\n".join(pretty_lines)
        try:
            with open(output_path, "w") as f:
                xml_file = f.write(pretty_xml)
        except Exception as e:
            raise Exception(f"An error occurred: {e}")


# How to use this class:
# xml_formatter = XMLFormatter("path/to/input.xml")
# valid = xml_formatter.prettify("path/to/output.xml")
# if valid:
#     print("File was successfully written")
# else:
#     print(valid)
