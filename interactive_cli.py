import subprocess
import sys
import os
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def resource_path(relative_path):
    """Get the absolute path to a resource, works for PyInstaller"""
    if getattr(sys, '_MEIPASS', False):  # If running in a PyInstaller bundle
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def print_ascii_banner():
    banner = """
{}                                                                                                                    
                                      ::                                                                                
                                      %%                                                                                
                                      %%                                                                                
   #*:*##%#+.    -*###%#=     -*%###+:%%   .=#####+:   .+#%%%#+:    =*%%%%#+.   .=*%%%%#=.   *#+=#%%%#=.    :+#%%%#+:   
   %%#.   -%#   #%-    :#%.  +%+    -%%%  :%#     *%- .%%%:.-**=  .%%%#)%%%.   -%%%    %%%:  #%%%*==*%%%:  =%%#   *%%=  
   %%      #%  *%-      .%# :%+      .%%  %%=::::::%%  #%%+-:.    *%%:        .%%%:    .%%#  #%%.    :%%% :%%%=====#%%  
   %#      *%  %%.       #% =%-       %% .%%=========   -+*#%%%+  #%%         .%%#      *%%  #%*      #%%.-%%. 
   %#      *%  =%+      -%+ .%#      =%%  *%-      -. .-+:   +%%- =%%+.   =+-. #%%+.  .=%%*  #%%=   .+%%*  %%%:    ==.  
   %#      *%   :##=--=#%=   :#%+--=#*%%   =%*=--+%#: .*%%%##%%*   =#%%%%%%%+   +%%%%%%%%=   #%%#%%%%%%=   .*%%%#%%%#:  
   --      :-     :-===:       .===-. --     :===-.     .-===-.      :-===-       :====:     #%# :===-        -===-.    
                                                                                             #%#                        
                                                                                             #%#                        
                                                                                                                       
                                     Nodescope: an XML Editor and Visualizer                                                                                                                
{}""".format(Fore.CYAN, Style.RESET_ALL)
    print(banner)

def interactive_loop():
    print_ascii_banner()
    try:
        from src.cli.cli_handler import main as cli_main  # Import the CLI handler's main function
    except ImportError as e:
        print(f"{Fore.RED}Error importing CLI handler: {e}{Style.RESET_ALL}")
        sys.exit(1)
    
    while True:
        try:
            command = input(f"{Fore.GREEN}>> {Style.RESET_ALL}").strip()
            if command.lower() in ["exit", "quit"]:
                print(f"{Fore.LIGHTRED_EX}Exiting CLI mode. Goodbye!{Style.RESET_ALL}")
                sys.exit(0)
            elif not command:
                continue  # Skip empty commands
            
            # Split the command into arguments
            args = command.split()
            
            # Backup original sys.argv
            original_argv = sys.argv.copy()
            
            # Set sys.argv to mimic command-line arguments
            sys.argv = [sys.executable, *args]
            
            try:
                cli_main()  # Call the CLI handler's main function
            except SystemExit:
                # argparse may call sys.exit(), which raises SystemExit
                pass
            finally:
                # Restore original sys.argv
                sys.argv = original_argv
        except KeyboardInterrupt:
            print(f"\n{Fore.LIGHTRED_EX}Exiting CLI mode. Goodbye!{Style.RESET_ALL}")
            sys.exit(0)
        except Exception as e:
            print(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    interactive_loop()
