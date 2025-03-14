import argparse
import subprocess
import sys, os
from colorama import init, Fore, Style
from interactive_cli import interactive_loop

# Initialize colorama
init(autoreset=True)

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for PyInstaller """
    if getattr(sys, '_MEIPASS', False):  # If running in a PyInstaller bundle
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

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
    interactive_loop()

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