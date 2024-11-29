import customtkinter as ctk
from PIL import Image

from guimodules.WelcomeFrame import WelcomeFrame
from guimodules.FileInputFrame import FileInputFrame
from guimodules.OperationsFrame import OperationsFrame
from guimodules.OutputFrame import OutputFrame


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("NodeScope")
        self.geometry("1000x700")

        # Center the window
        self.center_window()

        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Initialize variables
        self.file_path = None
        self.xml_content = None

        # Load images (placeholders - replace paths with actual images)
        self.load_images()

        # Create frames
        self.frames = {}
        self.current_frame = None
        self.create_frames()
        self.show_frame("WelcomeFrame")

    def center_window(self):
        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate window width and height
        window_width = 1000
        window_height = 700

        # Calculate position x and y coordinates
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Set the window position
        self.geometry(f'{window_width}x{window_height}+{x}+{y}')

    def load_images(self):
        # Placeholder for image loading - replace with actual paths
        self.light_logo_path = r"../../assets/images/nodescope_light.png"
        self.dark_logo_path = r"../../assets/images/nodescope_dark.png"

        # Load placeholder images (replace with actual images)
        try:
            self.logo_image = ctk.CTkImage(
                light_image=Image.open(self.dark_logo_path),
                dark_image=Image.open(self.light_logo_path),
                size=(500, 150)
            )
        except Exception as e:
                print(f"Error loading logo image: {e}")
                self.logo_image = None

    def create_frames(self):
        """Create and initialize all application frames"""
        # Dictionary to store frame classes
        frame_classes = {
            "WelcomeFrame": WelcomeFrame,
            "FileInputFrame": FileInputFrame,
            "OperationsFrame": OperationsFrame,
            "OutputFrame": OutputFrame
        }

        # Create an instance of each frame
        for frame_name, frame_class in frame_classes.items():
            frame = frame_class(self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[frame_name] = frame
            frame.grid_remove()  # Hide all frames initially

    def show_frame(self, frame_name):
        """Switch to the specified frame"""
        # Hide current frame if it exists
        if self.current_frame:
            self.frames[self.current_frame].grid_remove()

        # Show the requested frame
        self.frames[frame_name].grid()
        self.current_frame = frame_name


if __name__ == "__main__":
    app = App()
    app.mainloop()
