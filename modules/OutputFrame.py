import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog

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

        # Format selection
        format_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        format_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))

        format_label = ctk.CTkLabel(
            format_frame,
            text="Save as:",
            font=ctk.CTkFont(size=13)
        )
        format_label.pack(side="left", padx=(0, 10))

        self.format_var = tk.StringVar(value="xml")

        xml_radio = ctk.CTkRadioButton(
            format_frame,
            text="XML",
            variable=self.format_var,
            value="xml"
        )
        xml_radio.pack(side="left", padx=10)

        json_radio = ctk.CTkRadioButton(
            format_frame,
            text="JSON",
            variable=self.format_var,
            value="json"
        )
        json_radio.pack(side="left", padx=10)

        compressed_radio = ctk.CTkRadioButton(
            format_frame,
            text="Compressed",
            variable=self.format_var,
            value="compressed"
        )
        compressed_radio.pack(side="left", padx=10)

        # Button frame
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.grid(row=3, column=0, pady=20)

        # Copy button
        copy_button = ctk.CTkButton(
            button_frame,
            text="Copy to Clipboard",
            width=140,
            height=40,
            command=self.copy_to_clipboard,
            fg_color="#6366f1",  # Indigo color
            hover_color="#4f46e5"
        )
        copy_button.pack(side="left", padx=10)

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

    def copy_to_clipboard(self):
        content = self.output_text.get("1.0", tk.END)
        self.clipboard_clear()
        self.clipboard_append(content)

        # Show temporary success message
        original_text = self.status_label.cget("text")
        original_color = self.status_label.cget("text_color")

        self.status_label.configure(text="Copied to clipboard!", text_color="#10b981")
        self.after(2000, lambda: self.status_label.configure(
            text=original_text,
            text_color=original_color
        ))

    def save_output(self):
        file_format = self.format_var.get()
        extensions = {
            "xml": ".xml",
            "json": ".json",
            "compressed": ".gz"
        }

        filename = filedialog.asksaveasfilename(
            defaultextension=extensions[file_format],
            filetypes=[
                ("XML files", "*.xml"),
                ("JSON files", "*.json"),
                ("Compressed files", "*.gz"),
                ("All files", "*.*")
            ]
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    content = self.output_text.get("1.0", tk.END)
                    f.write(content)

                self.status_label.configure(
                    text="File saved successfully!",
                    text_color="#10b981"
                )
                self.after(2000, lambda: self.status_label.configure(
                    text="Operation Complete",
                    text_color="#10b981"
                ))
            except Exception as e:
                self.status_label.configure(
                    text="Error saving file!",
                    text_color="#ef4444"
                )