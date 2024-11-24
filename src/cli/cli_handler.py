import argparse

class CLIHandler:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="XML Editor CLI")

    def setup_commands(self):
        self.parser.add_argument("command", help="The command to run (e.g., verify, format)")
        self.parser.add_argument("-i", "--input", required=True, help="Input file path")
        self.parser.add_argument("-o", "--output", help="Output file path")

    def execute(self):
        args = self.parser.parse_args()
        print(f"Command: {args.command}, Input: {args.input}, Output: {args.output}")
