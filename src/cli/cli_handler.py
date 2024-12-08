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
#TODO: modify parser handling
#TODO: Extension overriding 

def verify_xml(input_file, fix=False, output_file=None):
    print(f"{Style.BRIGHT}{Fore.CYAN}Verifying XML file: {input_file}{Style.RESET_ALL}")
    parser = XMLParser(input_file)  # Pass the input file to the XMLParser instance
    try:
        # First check for consistency
        error_count = parser.check_consistency()  # Returns number of errors found
        if error_count == 0:
            print(f"{Fore.GREEN}XML is valid.")
        else:
            print(f"{Fore.RED}XML is invalid. Errors found: {error_count}")
            for error_item in parser.errors:
                line = error_item[0]  # Line number where the error occurred
                error_message = error_item[1]  # The error message
                extra_info = error_item[2:]  # Additional info, if any

                print(f"  {Fore.YELLOW}Line {line}: {error_message}")
                if extra_info:
                    print(f"    {Fore.YELLOW}Additional info: {extra_info}")

            # If the --fix flag is set, fix errors
            if fix:
                parser.fix_errors()  # Fix the errors
                print(f"{Fore.GREEN}Errors fixed and saved to {input_file[:-4]}_fixed.xml")
            else:
                print(f"{Fore.RED}No fixes applied. Use --fix to correct the errors.")
    except Exception as e:
        print(f"{Fore.RED}Error during XML verification: {e}")


def format_xml(input_file, output_file):
    print(f"{Style.BRIGHT}{Fore.CYAN}Formatting XML file: {input_file}{Style.RESET_ALL}")
    formatter = XMLFormatter(input_file)
    try:
        formatter.prettify(output_file)
        print(f"{Fore.GREEN}Formatted XML saved to {output_file}")
    except Exception as e:
        print(f"{Fore.RED}Error during XML formatting: {e}")


def convert_to_json(input_file, output_file):
    print(f"{Style.BRIGHT}{Fore.CYAN}Converting XML file: {input_file} to JSON.{Style.RESET_ALL}")
    converter = XMLToJSONConverter(input_file)
    try:
        converter.convert(output_file)
        print(f"{Fore.GREEN}JSON saved to {output_file}")
    except Exception as e:
        print(f"{Fore.RED}Error during XML to JSON conversion: {e}")


def minify_xml(input_file, output_file):
    print(f"{Style.BRIGHT}{Fore.CYAN}Minifying XML file: {input_file}{Style.RESET_ALL}")
    minifier = XMLMinifier(input_file) 
    try:
        minifier.minify(output_file)
        print(f"{Fore.GREEN}Minified XML saved to {output_file}")
    except Exception as e:
        print(f"{Fore.RED}Error during XML minification: {e}")


def compress_xml(input_file, output_file):
    print(f"{Style.BRIGHT}{Fore.CYAN}Compressing XML file: {input_file}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}(Original File size: {os.path.getsize(input_file)} bytes)")
    compressor = XMLCompressor(input_file)
    try:
        compressor.compress(output_file)
        print(f"{Fore.GREEN}Compressed XML saved to {output_file}")
        print(f"{Fore.YELLOW}(Compressed File size: {os.path.getsize(output_file)} bytes)")
    except Exception as e:
        print(f"{Fore.RED}Error during XML compression: {e}")


def decompress_xml(input_file, output_file):
    print(f"{Style.BRIGHT}{Fore.CYAN}Decompressing file: {input_file}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}(Original File size: {os.path.getsize(input_file)} bytes)")
    decompressor = XMLDecompressor(input_file)
    try:
        decompressor.decompress(output_file)
        print(f"{Fore.GREEN}Decompressed XML saved to {output_file}")
        print(f"{Fore.YELLOW}(Decompressed File size: {os.path.getsize(output_file)} bytes)")
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

    mini_parser = subparsers.add_parser("minify", help="Minify XML")
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

    # Cascaded operations command
    cascade_parser = subparsers.add_parser("cascade", help="Perform cascaded operations")
    cascade_parser.add_argument("-i", "--input", required=True, help="Input XML file")
    cascade_parser.add_argument("-o", "--output", required=True, help="Final output file")
    cascade_parser.add_argument("-ops", "--operations", nargs='+', required=True, help="Sequence of operations (e.g., compress decompress)")

    args = parser.parse_args()

    if args.command == "verify":
        verify_xml(args.input, fix=args.fix, output_file=args.output)
    elif args.command == "format":
        format_xml(args.input, args.output)
    elif args.command == "json":
        convert_to_json(args.input, args.output)
    elif args.command == "mini" or args.command == "minify":
        minify_xml(args.input, args.output)
    elif args.command == "compress":
        compress_xml(args.input, args.output)
    elif args.command == "decompress":
        decompress_xml(args.input, args.output)
    elif args.command == "cascade":
        input_file = args.input
        intermediate_file = input_file
        for i, operation in enumerate(args.operations):
            output_file = f"{args.output}.tmp{i}"
            try:
                if operation == "compress":
                    compress_xml(intermediate_file, output_file)
                elif operation == "decompress":
                    decompress_xml(intermediate_file, output_file)
                elif operation == "minify":
                    minify_xml(intermediate_file, output_file)
                elif operation == "format":
                    format_xml(intermediate_file, output_file)
                elif operation == "json":
                    convert_to_json(intermediate_file, output_file)
                elif operation == "verify":
                    verify_xml(intermediate_file)
                else:
                    print(f"{Fore.RED}Error: Invalid operation {operation}")
                    return
            except Exception as e:
                print(f"{Fore.RED}Error during {operation}: {e}")
                return

            # Check if the output file was created successfully
            if not os.path.exists(output_file):
                print(f"{Fore.RED}Error: {operation} did not produce an output file.")
                return

            # Delete the intermediate temporary file after the operation is done
            if os.path.exists(intermediate_file):
                os.remove(intermediate_file)
            
            intermediate_file = output_file
        
        # Before renaming, check if the final output file exists
        if os.path.exists(args.output):
            os.remove(args.output)  # Delete the existing output file to avoid FileExistsError

        os.rename(intermediate_file, args.output)
        print(f"{Fore.GREEN}Cascaded operations completed. Final output saved to {args.output}")
        
    else:
        print(f"{Fore.RED}Error: Invalid command")
        parser.print_help()

if __name__ == "__main__":
    main()
