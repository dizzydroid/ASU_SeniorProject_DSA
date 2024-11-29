import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os


class OutputFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Create header
        header_frame = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))

        if parent.logo_image:
            small_logo = ctk.CTkLabel(header_frame, image=parent.logo_image, text="")
            small_logo.pack(side="left", padx=20)

        # Main content
        content_frame = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)  # Allow text area to expand

        # Status indicator
        self.status_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.status_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Operation Complete",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#10b981"  # Success green color
        )
        self.status_label.pack(side="left")

        # Output display
        self.output_text = ctk.CTkTextbox(
            content_frame,
            width=800,
            height=400,
            font=ctk.CTkFont(family="Courier", size=12)
        )
        self.output_text.grid(row=1, column=0, pady=(20, 20), padx=20, sticky="nsew")

        # Button frame
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.grid(row=3, column=0, pady=20)

        # Save button
        save_button = ctk.CTkButton(
            button_frame,
            text="Save Output",
            width=140,
            height=40,
            command=self.save_output,
            fg_color="#1f538d",
            hover_color="#14b8a6"
        )
        save_button.pack(side="left", padx=10)

        # Back button
        back_button = ctk.CTkButton(
            button_frame,
            text="Back to Operations",
            width=140,
            height=40,
            command=lambda: parent.show_frame("OperationsFrame"),
            fg_color="#6b7280",
            hover_color="#4b5563"
        )
        back_button.pack(side="left", padx=10)

        # Track the current file extension
        self.current_file_extension = ".xml"

    def save_output(self):
        try:
            # Determine file types and default extension
            file_types = [
                ("XML files", "*.xml"),
                ("JSON files", "*.json"),
                ("Compressed files", "*.zip"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]

            # Suggest filename based on current extension
            default_filename = f"output{self.current_file_extension}"

            # Open file dialog to choose save location
            filename = filedialog.asksaveasfilename(
                defaultextension=self.current_file_extension,
                filetypes=file_types,
                initialfile=default_filename
            )

            # If a filename is selected
            if filename:
                # Get content from text box
                content = self.output_text.get("1.0", tk.END).strip()

                # Write to file
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)

                # Update current file extension for next save
                self.current_file_extension = os.path.splitext(filename)[1]

                # Show success message
                self.status_label.configure(
                    text=f"File saved successfully as {os.path.basename(filename)}!",
                    text_color="#10b981"
                )
                # Revert status after 2 seconds
                self.after(2000, lambda: self.status_label.configure(
                    text="Operation Complete",
                    text_color="#10b981"
                ))

        except Exception as e:
            # Handle any errors during file saving
            self.status_label.configure(
                text=f"Error saving file: {str(e)}",
                text_color="#ef4444"
            )

    def set_current_extension(self, extension):
        """
        Method to set the current file extension from outside the class.
        Useful for tracking the type of last operation.
        """
        # Ensure extension starts with a dot
        self.current_file_extension = extension if extension.startswith('.') else f'.{extension}'