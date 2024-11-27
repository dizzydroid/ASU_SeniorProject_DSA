import sys
import os
from colorama import Fore, Style, init
# Add the project root to sys.path dynamically
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

# Initialize colorama
init(autoreset=True)

# cli args
import argparse
from src.modules.xml_parser import XMLParser
from src.modules.xml_formatter import XMLFormatter
from src.modules.xml_to_json import XMLToJSONConverter
from src.modules.xml_minifier import XMLMinifier
from src.modules.xml_compressor import XMLCompressor
from src.modules.xml_decompressor import XMLDecompressor

#TODO: Add logging

def verify_xml(input_file, fix=False, output_file=None):
    print(f"{Style.BRIGHT}{Fore.CYAN}Verifying XML file: {input_file}{Style.RESET_ALL}")
    parser = XMLParser()
    try:
        if fix:
            if output_file:
                parser.fix_errors(input_file, output_file)
                print(f"{Fore.GREEN}Fixed errors and saved the corrected XML to {output_file}")
            else:
                print(f"{Fore.RED}Error: Please provide an output file to save the corrected XML.")
        else:
            is_valid, errors = parser.check_consistency(input_file)
            if is_valid:
                print(f"{Fore.GREEN}XML is valid.")
            else:
                print(f"{Fore.RED}XML is invalid. Errors found:")
                for line, error in errors.items():
                    print(f"  {Fore.YELLOW}Line {line}: {error}")
    except Exception as e:
        print(f"{Fore.RED}Error during XML verification: {e}")


def format_xml(input_file, output_file):
    print(f"{Style.BRIGHT}{Fore.CYAN}Formatting XML file: {input_file}{Style.RESET_ALL}")
    formatter = XMLFormatter()
    try:
        formatter.prettify(input_file, output_file)
        print(f"{Fore.GREEN}Formatted XML saved to {output_file}")
    except Exception as e:
        print(f"{Fore.RED}Error during XML formatting: {e}")


def convert_to_json(input_file, output_file):
    print(f"{Style.BRIGHT}{Fore.CYAN}Converting XML file: {input_file} to JSON.{Style.RESET_ALL}")
    converter = XMLToJSONConverter(input_file)
    try:
        converter.convert(output_file)
        print(f"{Fore.GREEN}✅ JSON saved to {output_file}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error during XML to JSON conversion: {e}")


def minify_xml(input_file, output_file):
    print(f"{Style.BRIGHT}{Fore.CYAN}Minifying XML file: {input_file}{Style.RESET_ALL}")
    minifier = XMLMinifier()
    try:
        minifier.minify(input_file, output_file)
        print(f"{Fore.GREEN}Minified XML saved to {output_file}")
    except Exception as e:
        print(f"{Fore.RED}Error during XML minification: {e}")


def compress_xml(input_file, output_file):
    print(f"{Style.BRIGHT}{Fore.CYAN}Compressing XML file: {input_file}{Style.RESET_ALL}")
    compressor = XMLCompressor()
    try:
        compressor.compress(input_file, output_file)
        print(f"{Fore.GREEN}Compressed XML saved to {output_file}")
    except Exception as e:
        print(f"{Fore.RED}Error during XML compression: {e}")


def decompress_xml(input_file, output_file):
    print(f"{Style.BRIGHT}{Fore.CYAN}Decompressing file: {input_file}{Style.RESET_ALL}")
    decompressor = XMLDecompressor()
    try:
        decompressor.decompress(input_file, output_file)
        print(f"{Fore.GREEN}Decompressed XML saved to {output_file}")
    except Exception as e:
        print(f"{Fore.RED}Error during decompression: {e}")



def main():
    parser = argparse.ArgumentParser(description="XML Editor CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Check XML consistency")
    verify_parser.add_argument("-i", "--input", required=True, help="Input XML file")
    verify_parser.add_argument("-f", "--fix", action="store_true", help="Fix errors in XML")
    verify_parser.add_argument("-o", "--output", help="Output file for fixed XML")

    # Format command
    format_parser = subparsers.add_parser("format", help="Prettify XML")
    format_parser.add_argument("-i", "--input", required=True, help="Input XML file")
    format_parser.add_argument("-o", "--output", required=True, help="Output formatted XML file")

    # JSON command
    json_parser = subparsers.add_parser("json", help="Convert XML to JSON")
    json_parser.add_argument("-i", "--input", required=True, help="Input XML file")
    json_parser.add_argument("-o", "--output", required=True, help="Output JSON file")

    # Minify command
    mini_parser = subparsers.add_parser("mini", help="Minify XML")
    mini_parser.add_argument("-i", "--input", required=True, help="Input XML file")
    mini_parser.add_argument("-o", "--output", required=True, help="Output minified XML file")

    # Compress command
    compress_parser = subparsers.add_parser("compress", help="Compress XML")
    compress_parser.add_argument("-i", "--input", required=True, help="Input XML file")
    compress_parser.add_argument("-o", "--output", required=True, help="Output compressed file")

    # Decompress command
    decompress_parser = subparsers.add_parser("decompress", help="Decompress XML")
    decompress_parser.add_argument("-i", "--input", required=True, help="Input compressed file")
    decompress_parser.add_argument("-o", "--output", required=True, help="Output XML file")

    args = parser.parse_args()

    if args.command == "verify":
        verify_xml(args.input, fix=args.fix, output_file=args.output)
    elif args.command == "format":
        format_xml(args.input, args.output)
    elif args.command == "json":
        convert_to_json(args.input, args.output)
    elif args.command == "mini":
        minify_xml(args.input, args.output)
    elif args.command == "compress":
        compress_xml(args.input, args.output)
    elif args.command == "decompress":
        decompress_xml(args.input, args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
