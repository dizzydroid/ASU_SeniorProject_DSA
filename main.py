import sys
from src.cli.cli_handler import CLIHandler
from src.gui.gui_handler import GUIHandler

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        CLIHandler().run()
    else:
        GUIHandler().run()

if __name__ == "__main__":
    main()
