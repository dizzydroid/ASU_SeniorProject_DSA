import customtkinter as ctk

class WelcomeFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Create main container
        self.container = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        self.container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.container.grid_columnconfigure(0, weight=1)

        # Logo placeholder
        if parent.logo_image:
            logo_label = ctk.CTkLabel(self.container, image=parent.logo_image, text="")
            logo_label.grid(row=0, column=0, pady=20)

        # Welcome message
        title = ctk.CTkLabel(
            self.container,
            text="XML Master",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=("#1f538d", "#14b8a6")
        )
        title.grid(row=1, column=0, pady=10)

        subtitle = ctk.CTkLabel(
            self.container,
            text="Advanced XML Processing Tool",
            font=ctk.CTkFont(size=16),
            text_color=("gray60", "gray40")
        )
        subtitle.grid(row=2, column=0, pady=5)

        # Start button with modern styling
        start_button = ctk.CTkButton(
            self.container,
            text="Get Started",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=lambda: parent.show_frame("FileInputFrame"),
            width=200,
            height=40,
            corner_radius=10,
            fg_color="#1f538d",
            hover_color="#14b8a6"
        )
        start_button.grid(row=3, column=0, pady=30)