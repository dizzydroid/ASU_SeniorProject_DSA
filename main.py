import argparse
import subprocess
import sys
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def launch_gui():
    from src.gui.gui_handler import App
    app = App()
    app.mainloop()

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

def launch_cli():
    print_ascii_banner()
    while True:
        try:
            # Prompt the user for input with styled text
            command = input(f"{Fore.GREEN}>> {Style.RESET_ALL}")
            if command.lower() in ["exit", "quit"]:
                print("Exiting CLI mode.")
                break
            # Pass the command to the CLI handler
            subprocess.run(["python", "src/cli/cli_handler.py"] + command.split(), check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nExiting CLI mode.")
            break

def main():
    parser = argparse.ArgumentParser(description="nodescope: an XML Editor and Visualizer")
    parser.add_argument("--gui", action="store_true", help="Launch GUI interface")
    parser.add_argument("--cli", action="store_true", help="Launch CLI interface")

    args = parser.parse_args()

    if args.gui:
        launch_gui()
    elif args.cli:
        launch_cli()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()