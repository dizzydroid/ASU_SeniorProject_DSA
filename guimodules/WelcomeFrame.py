from tkinter import Image
import customtkinter as ctk

class WelcomeFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Background container
        self.container = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        self.container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.container.grid_columnconfigure(0, weight=1)

        # Background image (optional)
        if hasattr(parent, 'bg_path') and parent.bg_path:
            try:
                bg_image = ctk.CTkImage(light_image=Image.open(parent.bg_path), size=(900, 700))
                bg_label = ctk.CTkLabel(self.container, image=bg_image, text="")
                bg_label.image = bg_image  # Keep a reference to prevent garbage collection
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            except Exception as e:
                print(f"Error loading background image: {e}")  # Log the error for debugging

        # Centered content
        content_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Logo placeholder
        if hasattr(parent, 'logo_image') and parent.logo_image:
            logo_label = ctk.CTkLabel(content_frame, image=parent.logo_image, text="")
            logo_label.grid(row=0, column=0, pady=20)

        # Welcome message
        title = ctk.CTkLabel(
            content_frame,
            text="Welcome to NodeScope",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#1f538d",
        )
        title.grid(row=1, column=0, pady=10)

        subtitle = ctk.CTkLabel(
            content_frame,
            text="Your go-to tool for XML processing",
            font=ctk.CTkFont(size=16),
            text_color=("gray60", "gray40"),
        )
        subtitle.grid(row=2, column=0, pady=5)

        # Start button
        start_button = ctk.CTkButton(
            content_frame,
            text="Get Started",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=lambda: parent.show_frame("FileInputFrame"),
            width=200,
            height=50,
            corner_radius=10,
            fg_color="#1f538d",
            hover_color="#14b8a6",
        )
        start_button.grid(row=3, column=0, pady=30)

        # Mode toggle button
        self.mode_toggle_button = ctk.CTkLabel(
            self,
            text="☀️",  # Sun emoji as a default
            font=ctk.CTkFont(size=30),
            text_color="#FFD700",  # Bright gold/yellow color
            bg_color="transparent",
            cursor="hand2"
        )
        self.mode_toggle_button.place(x=30, y=30)  # Position in top-left corner
        # Add click event
        self.mode_toggle_button.bind("<Button-1>", self.toggle_mode)

    def toggle_mode(self, event):
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Light":
            ctk.set_appearance_mode("Dark")
            self.mode_toggle_button.configure(text="☀️", text_color="#FFD700")
        else:
            ctk.set_appearance_mode("Light")
            self.mode_toggle_button.configure(text="🌙", text_color="#FFD700")
