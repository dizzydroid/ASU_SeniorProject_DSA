import sys
import os
from colorama import Fore, Style, init
import shutil

# Add the project root to sys.path dynamically
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

# cli args
import argparse
from src.modules.xml_parser import XMLParser
from src.modules.xml_formatter import XMLFormatter
from src.modules.xml_to_json import XMLToJSONConverter
from src.modules.xml_minifier import XMLMinifier
from src.modules.xml_compressor import XMLCompressor
from src.modules.xml_decompressor import XMLDecompressor
from src.graph.graph_representation import GraphRepresentation
from src.graph.network_analysis import NetworkAnalysis
from src.postsearch.post_search import PostSearch
from src.graph.graph_visualizer import GraphVisualizer
#TODO: Add logging

# Initialize colorama
init(autoreset=True)

# Utility function to handle file extensions
def add_extension(file_path, extension):
    if not file_path.endswith(extension):
        return f"{file_path}{extension}"
    return file_path

# Default output file function
def get_default_output(input_file, operation):
    # Determine default extension based on operation
    extension_map = {
        "json": ".json",
        "format": ".formatted.xml",
        "mini": ".minified.xml",
        "minify": ".minified.xml",
        "compress": ".compressed.xml",
        "decompress": ".decompressed.xml",
        "verify": "_fixed.xml"
    }
    
    extension = extension_map.get(operation, ".xml")  # Default to .xml if not found
    return add_extension(input_file, extension)


###### CLI commands (XML operations) ############################################################

def verify_xml(input_file, fix=False, output_file=None):
    print(f"{Style.BRIGHT}{Fore.CYAN}Verifying XML file: {input_file}{Style.RESET_ALL}")

    base_filename = os.path.splitext(input_file)[0]  # Get the base filename without extension
    if not output_file:
        output_file = f"{base_filename}_fixed.xml"

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
                output_file = output_file or get_default_output(input_file, "verify")
                print(f"{Fore.GREEN}Errors fixed and saved to {output_file}")
            else:
                print(f"{Fore.RED}No fixes applied. Please use --fix to correct the errors.")
                # Prompting the user to use verify --fix for fixing errors
                return False  # Return False to indicate that errors were not fixed
    except Exception as e:
        print(f"{Fore.RED}Error during XML verification: {e}")
        return False

    return True  # Return True if no errors found or errors were fixed



def format_xml(input_file, output_file):
    print(f"{Style.BRIGHT}{Fore.CYAN}Formatting XML file: {input_file}{Style.RESET_ALL}")

    base_filename = os.path.splitext(input_file)[0] # Get the base filename without extension
    if not output_file:
        output_file = f"{base_filename}_formatted.xml"

    formatter = XMLFormatter(input_file)
    try:
        output_file = output_file or get_default_output(input_file, "format")
        formatter.prettify(output_file)
        print(f"{Fore.GREEN}Formatted XML saved to {output_file}")
    except Exception as e:
        print(f"{Fore.RED}Error during XML formatting: {e}")


def convert_to_json(input_file, output_file):
    print(f"{Style.BRIGHT}{Fore.CYAN}Converting XML file: {input_file} to JSON.{Style.RESET_ALL}")

    base_filename = os.path.splitext(input_file)[0]  # Get the base filename without extension
    if not output_file:
        output_file = f"{base_filename}.json"

    try:
        converter = XMLToJSONConverter(input_file)
        output_file = output_file or get_default_output(input_file, "json")
        converter.convert(output_file)
        print(f"{Fore.GREEN}JSON saved to {output_file}")

    except Exception as e:
        # If an error occurs (likely due to invalid XML)
        print(f"{Fore.RED}Error during XML to JSON conversion: {e}")
        print(f"{Fore.YELLOW}It seems there is an issue with the XML format. Please verify and fix the XML using the 'verify' command.")
        print(f"{Fore.YELLOW}Example: `python cli_handler.py verify -i {input_file} -f` to fix errors.")



def minify_xml(input_file, output_file):
    print(f"{Style.BRIGHT}{Fore.CYAN}Minifying XML file: {input_file}{Style.RESET_ALL}")
    
    base_filename = os.path.splitext(input_file)[0] # Get the base filename without extension
    if not output_file:
        output_file = f"{base_filename}_minified.xml"

    minifier = XMLMinifier(input_file) 
    try:
        output_file = output_file or get_default_output(input_file, "minify")
        minifier.minify(output_file)
        print(f"{Fore.GREEN}Minified XML saved to {output_file}")
    except Exception as e:
        print(f"{Fore.RED}Error during XML minification: {e}")


def compress_xml(input_file, output_file):
    print(f"{Style.BRIGHT}{Fore.CYAN}Compressing XML file: {input_file}{Style.RESET_ALL}")

    base_filename = os.path.splitext(input_file)[0] # Get the base filename without extension
    if not output_file:
        output_file = f"{base_filename}_compressed.xml"

    print(f"{Fore.YELLOW}(Original File size: {os.path.getsize(input_file)} bytes)")
    compressor = XMLCompressor(input_file)
    try:
        output_file = output_file or get_default_output(input_file, "compress")
        compressor.compress(output_file)
        print(f"{Fore.GREEN}Compressed XML saved to {output_file}")
        print(f"{Fore.YELLOW}(Compressed File size: {os.path.getsize(output_file)} bytes)")
    except Exception as e:
        print(f"{Fore.RED}Error during XML compression: {e}")


def decompress_xml(input_file, output_file):
    print(f"{Style.BRIGHT}{Fore.CYAN}Decompressing file: {input_file}{Style.RESET_ALL}")

    base_filename = os.path.splitext(input_file)[0] # Get the base filename without extension
    if not output_file:
        output_file = f"{base_filename}_decompressed.xml"

    print(f"{Fore.YELLOW}(Original File size: {os.path.getsize(input_file)} bytes)")
    decompressor = XMLDecompressor(input_file)
    try:
        output_file = output_file or get_default_output(input_file, "decompress")
        decompressor.decompress(output_file)
        print(f"{Fore.GREEN}Decompressed XML saved to {output_file}")
        print(f"{Fore.YELLOW}(Decompressed File size: {os.path.getsize(output_file)} bytes)")
    except Exception as e:
        print(f"{Fore.RED}Error during decompression: {e}")

def cascade_operations(input_file, output_file, operations):
    # Check if the input file has an extension, if not, append '.xml'
    if not os.path.splitext(input_file)[1]:
        input_file = f"{input_file}.xml"  # Append .xml if no extension is present
    print(f"{Fore.LIGHTYELLOW_EX}You forgot to add the extension to the input file :) \nAppending '.xml' to the input file name.")

    intermediate_file = input_file  # Start with the original input file
    final_output_extension = '.xml'  # Default extension for output files
    
    for i, operation in enumerate(operations):
        # Generate intermediate output file with a unique name
        temp_output_file = f"{output_file}.tmp{i}"
        
        try:
            if operation == "compress":
                compress_xml(intermediate_file, temp_output_file)
            elif operation == "decompress":
                decompress_xml(intermediate_file, temp_output_file)
            elif operation == "minify":
                minify_xml(intermediate_file, temp_output_file)
            elif operation == "format":
                format_xml(intermediate_file, temp_output_file)
            elif operation == "json":
                convert_to_json(intermediate_file, temp_output_file)
                final_output_extension = '.json'  # If 'json' operation is performed, change extension
            elif operation == "verify":
                # If the operation is 'verify', don't expect an output file
                verify_xml(intermediate_file, fix=False)  # Just validate
                print(f"{Fore.LIGHTMAGENTA_EX}XML verification passed for {intermediate_file}")
                continue  # Skip file output for verify
            else:
                print(f"{Fore.RED}Error: Invalid operation {operation}")
                return

        except Exception as e:
            print(f"{Fore.RED}Error during {operation}: {e}")
            return

        # After the operation, check if the output file was created successfully
        if not os.path.exists(temp_output_file):
            print(f"{Fore.RED}Error: {operation} did not produce an output file.")
            return

        # Remove the original file if it's an intermediate step, but not the input file
        if os.path.exists(intermediate_file) and intermediate_file != input_file:
            os.remove(intermediate_file)

        # Set the intermediate file to the new temp_output_file for the next operation
        intermediate_file = temp_output_file
    
    # Check if user provided an output file name with -o
    if output_file:
        # If the user provided -o but the extension is not correct, append the correct one
        if not output_file.endswith(final_output_extension):
            output_file = f"{output_file}{final_output_extension}"
    else:
        # If no output file was provided, default to using the final extension
        output_file = f"{output_file}{final_output_extension}"

    # Check if the user has already specified the correct extension in -o
    if final_output_extension == '.json' and not output_file.endswith('.json'):
        output_file = f"{output_file}.json"

    # Before renaming, check if the final output file exists
    if os.path.exists(output_file):
        os.remove(output_file)  # Delete the existing output file to avoid FileExistsError

    # Clean up temporary files
    temp_files = [f"{output_file}.tmp{i}" for i in range(len(operations))]
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    # Set the final output file name with the correct extension
    final_output_file = output_file  # It's already fixed here

    # Move the last intermediate file to the final output location
    shutil.move(intermediate_file, final_output_file)
    print(f"{Fore.LIGHTGREEN_EX}\nCascaded operations completed. Final output saved to {final_output_file}")


###### CLI commands (Graph Related) ############################################################
def draw_graph(input_file, output_file):
    print(f"{Style.BRIGHT}{Fore.CYAN}Visualizing Graph: {input_file}{Style.RESET_ALL}")
    if not os.path.splitext(input_file)[1]:
        input_file = f"{input_file}.xml"  # Append .xml if no extension is present
        print(f"{Fore.LIGHTYELLOW_EX}You forgot to add the extension to the input file :) \nAppending '.xml' to the input file name.")
    try:
        graph = GraphRepresentation.build_graph(input_file)
        GraphVisualizer(graph).visualize(save_path=output_file)
        print(f"{Fore.GREEN}Graph Visualization saved to {output_file}")
    except Exception as e:
        print(f"{Fore.RED}Error: did not produce an output file.")

def most_active_user(input_file):
    print(f"{Style.BRIGHT}{Fore.CYAN}Finding most active user: {input_file}{Style.RESET_ALL}")
    if not os.path.splitext(input_file)[1]:
        input_file = f"{input_file}.xml"  # Append .xml if no extension is present
        print(f"{Fore.LIGHTYELLOW_EX}You forgot to add the extension to the input file :) \nAppending '.xml' to the input file name.")
    try:
        graph = GraphRepresentation.build_graph(input_file)
        user = NetworkAnalysis(graph).get_most_active_user() 
        print(f"Most active user: {user}")
    except Exception as e:
        print(f"{Fore.RED}Error finding most active user: {e}")

def most_influencer_user(input_file):
    print(f"{Style.BRIGHT}{Fore.CYAN}Finding most influential user: {input_file}{Style.RESET_ALL}")
    if not os.path.splitext(input_file)[1]:
        input_file = f"{input_file}.xml"  # Append .xml if no extension is present
        print(f"{Fore.LIGHTYELLOW_EX}You forgot to add the extension to the input file :) \nAppending '.xml' to the input file name.")
    try:
        graph = GraphRepresentation.build_graph(input_file)
        user = NetworkAnalysis(graph).get_most_influencer_user()
        print(f"Most influential user: {user}")
    except Exception as e:
        print(f"{Fore.RED}Error finding most influential user: {e}")

def mutual_users(input_file, ids):
    print(f"{Style.BRIGHT}{Fore.CYAN}Finding mutual users for IDs {ids} in {input_file}{Style.RESET_ALL}")
    try:
        graph = GraphRepresentation.build_graph(input_file)
        analyzer = NetworkAnalysis(graph)
        mutuals = analyzer.get_mutual_users(ids)
        print(f"Mutual users: {mutuals}")
    except Exception as e:
        print(f"{Fore.RED}Error finding mutual users: {e}")

def suggest_users(input_file, user_id):
    print(f"{Style.BRIGHT}{Fore.CYAN}Suggesting users for user ID {user_id} in {input_file}{Style.RESET_ALL}")
    try:
        graph = GraphRepresentation.build_graph(input_file)
        analyzer = NetworkAnalysis(graph)
        suggestions = analyzer.get_suggested_users(user_id)
        print(f"Suggested users: {suggestions}")
    except Exception as e:
        print(f"{Fore.RED}Error suggesting users: {e}")

def search_posts(input_file, word=None, topic=None):
    print(f"Searching posts in {input_file}")
    try:
        searcher = PostSearch(input_file)
        if word:
            results = searcher.search_by_word(word)
            print(f"Posts containing the word '{word}': {results}")
        elif topic:
            results = searcher.search_by_topic(topic)
            print(f"Posts related to the topic '{topic}': {results}")
    except Exception as e:
        print(f"Error searching posts: {e}")


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
    format_parser.add_argument("-o", "--output", help="Output formatted XML file")

    # JSON command
    json_parser = subparsers.add_parser("json", help="Convert XML to JSON")
    json_parser.add_argument("-i", "--input", required=True, help="Input XML file")
    json_parser.add_argument("-o", "--output", help="Output JSON file")

    # Minify command
    mini_parser = subparsers.add_parser("mini", help="Minify XML")
    mini_parser.add_argument("-i", "--input", required=True, help="Input XML file")
    mini_parser.add_argument("-o", "--output", help="Output minified XML file")

    mini_parser = subparsers.add_parser("minify", help="Minify XML")
    mini_parser.add_argument("-i", "--input", required=True, help="Input XML file")
    mini_parser.add_argument("-o", "--output", help="Output minified XML file")

    # Compress command
    compress_parser = subparsers.add_parser("compress", help="Compress XML")
    compress_parser.add_argument("-i", "--input", required=True, help="Input XML file")
    compress_parser.add_argument("-o", "--output", help="Output compressed file")

    # Decompress command
    decompress_parser = subparsers.add_parser("decompress", help="Decompress XML")
    decompress_parser.add_argument("-i", "--input", required=True, help="Input compressed file")
    decompress_parser.add_argument("-o", "--output", help="Output XML file")

    # Cascaded operations command
    cascade_parser = subparsers.add_parser("cascade", help="Perform cascaded operations")
    cascade_parser.add_argument("-i", "--input", required=True, help="Input XML file")
    cascade_parser.add_argument("-o", "--output", required=True, help="Final output file")
    cascade_parser.add_argument("-ops", "--operations", nargs='+', required=True, help="Sequence of operations (e.g., compress decompress)")

    # Graph representation command
    draw_parser = subparsers.add_parser("draw", help="Draw XML data as a graph")
    draw_parser.add_argument("-i", "--input", required=True, help="Input XML file")
    draw_parser.add_argument("-o", "--output", required=True, help="Output image file")

    # Network analysis commands
    most_active_parser = subparsers.add_parser("most_active", help="Find most active user")
    most_active_parser.add_argument("-i", "--input", required=True, help="Input XML file")

    most_influencer_parser = subparsers.add_parser("most_influencer", help="Find most influential user")
    most_influencer_parser.add_argument("-i", "--input", required=True, help="Input XML file")

    mutual_parser = subparsers.add_parser("mutual", help="Find mutual users")
    mutual_parser.add_argument("-i", "--input", required=True, help="Input XML file")
    mutual_parser.add_argument("-ids", required=True, help="Comma-separated user IDs")

    suggest_parser = subparsers.add_parser("suggest", help="Suggest users for a given user ID")
    suggest_parser.add_argument("-i", "--input", required=True, help="Input XML file")
    suggest_parser.add_argument("-id", required=True, help="User ID")

    # Post search commands
    search_parser = subparsers.add_parser("search", help="Search posts")
    search_parser.add_argument("-i", "--input", required=True, help="Input XML file")
    search_parser.add_argument("-w", "--word", help="Word to search for in posts")
    search_parser.add_argument("-t", "--topic", help="Topic to search for in posts")

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
        cascade_operations(args.input, args.output, args.operations)
    
    elif args.command == "draw":
        draw_graph(args.input, args.output)
    elif args.command == "most_active":
        most_active_user(args.input)
    elif args.command == "most_influencer":
        most_influencer_user(args.input)
    elif args.command == "mutual":
        mutual_users(args.input, args.ids.split(","))
    elif args.command == "suggest":
        suggest_users(args.input, args.id)
    elif args.command == "search":
        search_posts(args.input, args.word, args.topic)
              
    else:
        print(f"{Fore.RED}Error: Invalid command")
        parser.print_help()



if __name__ == "__main__":
    main()
