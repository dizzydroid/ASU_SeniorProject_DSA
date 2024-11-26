import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog

class FileInputFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Create header
        header_frame = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))
        header_frame.grid_columnconfigure(1, weight=1)

        # Add title to header
        title_label = ctk.CTkLabel(
            header_frame,
            text="XML File Input",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left", padx=20, pady=10)

        # Main content frame
        self.content_frame = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(2, weight=1)  # Make text area expandable

        # File input section with better spacing
        input_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        input_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        input_frame.grid_columnconfigure(1, weight=1)

        # File path entry
        self.file_path_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Select XML File...",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.file_path_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10), columnspan=2)

        # Browse button
        browse_button = ctk.CTkButton(
            input_frame,
            text="Browse",
            width=100,
            command=self.browse_file,
            fg_color="#1f538d",
            hover_color="#14b8a6"
        )
        browse_button.grid(row=0, column=2, padx=(10, 0))

        # Preview section
        preview_label = ctk.CTkLabel(
            self.content_frame,
            text="XML Content Preview",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        preview_label.grid(row=1, column=0, pady=(20, 10), sticky="w", padx=20)

        # XML content preview
        self.xml_text = ctk.CTkTextbox(
            self.content_frame,
            width=800,
            height=300,
            font=ctk.CTkFont(family="Courier", size=12)
        )
        self.xml_text.grid(row=2, column=0, pady=(0, 20), padx=20, sticky="nsew")

        # Navigation buttons frame
        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        button_frame.grid(row=3, column=0, pady=(0, 20), padx=20)

        # Back button
        self.back_button = ctk.CTkButton(
            button_frame,
            text="Back",
            width=100,
            command=lambda: parent.show_frame("WelcomeFrame"),
            fg_color="#6b7280",
            hover_color="#4b5563"
        )
        self.back_button.pack(side="left", padx=10)

        # Continue button
        self.continue_button = ctk.CTkButton(
            button_frame,
            text="Continue",
            width=100,
            command=self.proceed_to_operations,
            fg_color="#1f538d",
            hover_color="#14b8a6",
            state="disabled"  # Initially disabled until file is loaded
        )
        self.continue_button.pack(side="left", padx=10)

    def browse_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
        )
        if filename:
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, filename)

            try:
                # Read and display file content
                with open(filename, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.xml_text.delete("1.0", tk.END)
                    self.xml_text.insert("1.0", content)

                # Enable continue button
                self.continue_button.configure(state="normal")

                # Store file path in parent
                self.parent.file_path = filename

                # Show success message
                self.show_status("File loaded successfully!", "success")
            except Exception as e:
                self.show_status(f"Error loading file: {str(e)}", "error")
                self.continue_button.configure(state="disabled")

    def proceed_to_operations(self):
        if self.parent.file_path:  # Only proceed if we have a file
            self.parent.show_frame("OperationsFrame")
        else:
            self.show_status("Please select a file first!", "error")

    def show_status(self, message, status_type="info"):
        colors = {
            "info": "#3b82f6",
            "success": "#10b981",
            "error": "#ef4444"
        }

        # Create status frame if it doesn't exist
        if not hasattr(self, 'status_label'):
            status_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            status_frame.grid(row=4, column=0, pady=(0, 10))
            self.status_label = ctk.CTkLabel(
                status_frame,
                text="",
                font=ctk.CTkFont(size=13)
            )
            self.status_label.pack()

        # Update status message
        self.status_label.configure(
            text=message,
            text_color=colors.get(status_type, colors["info"])
        )

        # Clear status after 3 seconds
        self.after(3000, lambda: self.status_label.configure(text=""))