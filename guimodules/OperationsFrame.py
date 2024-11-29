import customtkinter as ctk


class OperationsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Create header
        header_frame = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(12, 0))

        if parent.logo_image:
            small_logo = ctk.CTkLabel(header_frame, image=parent.logo_image, text="")
            small_logo.pack(side="left", padx=20)

        # Main content
        content_frame = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        content_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)

        # Operations
        operations = [
            {
                "title": "Check XML Consistency",
                "description": "Validate XML structure and detect errors",
                "icon": "🔍"
            },
            {
                "title": "Format XML",
                "description": "Beautify and organize XML structure",
                "icon": "✨"
            },
            {
                "title": "Convert to JSON",
                "description": "Transform XML to JSON format",
                "icon": "🔄"
            },
            {
                "title": "Minify XML",
                "description": "Compress XML by removing whitespace",
                "icon": "📝"
            },
            {
                "title": "Compress Data",
                "description": "Reduce file size while preserving content",
                "icon": "📦"
            },
            {
                "title": "Decompress Data",
                "description": "Restore compressed data to original format",
                "icon": "📨"
            }
        ]

        # Create operation cards
        for i, op in enumerate(operations):
            self.create_operation_card(
                content_frame,
                op["title"],
                op["description"],
                op["icon"],
                i // 2,
                i % 2
            )

        # Navigation button

        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=20, sticky="ew")

        # Create a container to center the buttons
        center_container = ctk.CTkFrame(button_frame, fg_color="transparent")
        center_container.pack(expand=True, anchor="center")

        back_button = ctk.CTkButton(
            center_container,
            text="Back",
            width=140,
            command=lambda: parent.show_frame("FileInputFrame"),  # Go back to FileInputFrame
            fg_color="#6b7280",
            hover_color="#4b5563"
        )
        back_button.pack(side="left", padx=10)

    def create_operation_card(self, parent, title, description, icon, row, col):
        """Creates a card for each operation"""
        card = ctk.CTkFrame(parent, fg_color=("#f8fafc", "#2d3748"))
        card.grid(row=row, column=col, padx=10, pady=4, sticky="nsew")

        # Icon and title
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 5))

        icon_label = ctk.CTkLabel(
            header_frame,
            text=icon,
            font=ctk.CTkFont(size=24)
        )
        icon_label.pack(side="left")

        title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(side="left", padx=10)

        # Description
        desc_label = ctk.CTkLabel(
            card,
            text=description,
            font=ctk.CTkFont(size=12),
            text_color=("gray60", "gray40")
        )
        desc_label.pack(padx=15, pady=(0, 10))

        # Execute button
        execute_button = ctk.CTkButton(
            card,
            text="Execute",
            width=120,
            height=32,
            command=lambda t=title: self.execute_operation(t),
            fg_color="#1f538d",
            hover_color="#14b8a6"
        )
        execute_button.pack(pady=(0, 15))

    def execute_operation(self, operation):
        """Placeholder for operation execution logic"""
        print(f"Executing: {operation}")