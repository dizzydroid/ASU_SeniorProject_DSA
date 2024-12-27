import json
from tkinter import messagebox
import customtkinter as ctk
import os
import networkx as nx

from src.modules.xml_parser import XMLParser
from src.modules.xml_formatter import XMLFormatter
from src.modules.xml_to_json import XMLToJSONConverter
from src.modules.xml_minifier import XMLMinifier
from src.modules.xml_compressor import XMLCompressor
from src.modules.xml_decompressor import XMLDecompressor
from src.graph.graph_representation import GraphRepresentation
from src.graph.network_analysis import NetworkAnalysis
from src.postsearch.post_search import PostSearch

from src.graph.graph_representation import GraphRepresentation
from src.graph.network_analysis import NetworkAnalysis
from src.graph.graph_visualizer import GraphVisualizer
from src.postsearch.post_search import PostSearch




class OperationsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent

        # Pagination state
        self.current_page = 0
        self.items_per_page = 6

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Create header
        header_frame = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(12, 0))

        if parent.logo_image:
            small_logo = ctk.CTkLabel(header_frame, image=parent.logo_image, text="")
            small_logo.pack(side="left", padx=20)

        # Main content frame setup
        self.content_frame = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)

        # Configure content frame grid
        for i in range(3):  # 3 rows for 6 cards (2 columns)
            self.content_frame.grid_rowconfigure(i, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)

        # All operations
        self.operations = [
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
            },
            {
                "title": "Draw Graph",
                "description": "Represent XML as a graph visualization",
                "icon": "📊"
            },
            {
                "title": "Most Active User",
                "description": "Find the most active user in the network",
                "icon": "👤"
            },
            {
                "title": "Top Influencer",
                "description": "Identify the most influential user",
                "icon": "⭐"
            },
            {
                "title": "Mutual Users",
                "description": "Find mutual users between specified IDs",
                "icon": "🤝"
            },
            {
                "title": "User Suggestions",
                "description": "Get user recommendations",
                "icon": "💡"
            },
            {
                "title": "Word Search",
                "description": "Search posts for specific words",
                "icon": "🔍"
            },
            {
                "title": "Topic Search",
                "description": "Search posts by topic",
                "icon": "📑"
            }
        ]

        # Navigation frame (now properly placed after content_frame)
        self.nav_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.nav_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        # Center container for navigation elements
        nav_center = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        nav_center.pack(expand=True, fill="x")

        # Navigation buttons with page indicator
        self.prev_button = ctk.CTkButton(
            nav_center,
            text="←",
            width=40,
            command=self.prev_page,
            fg_color="#1f538d",
            hover_color="#14b8a6"
        )
        self.prev_button.pack(side="left", padx=10)

        # Page indicator
        self.page_indicator = ctk.CTkLabel(
            nav_center,
            text="Page 1",
            font=ctk.CTkFont(size=12)
        )
        self.page_indicator.pack(side="left", padx=10)

        self.next_button = ctk.CTkButton(
            nav_center,
            text="→",
            width=40,
            command=self.next_page,
            fg_color="#1f538d",
            hover_color="#14b8a6"
        )
        self.next_button.pack(side="left", padx=10)

        # Back button frame (modify this section in your OperationsFrame class)
        button_frame = ctk.CTkFrame(self, fg_color="transparent")  # Changed parent from self.content_frame to self
        button_frame.grid(row=2, column=0, pady=10, sticky="ew")  # Changed grid layout

        # Create back button directly in button frame
        back_button = ctk.CTkButton(
            button_frame,
            text="Back",
            width=140,
            command=lambda: parent.show_frame("FileInputFrame"),
            fg_color="#6b7280",
            hover_color="#4b5563"
        )
        back_button.pack(expand=True)  # Changed to pack with expand

        # Initial display
        self.update_operations_display()

    def update_operations_display(self):
        # Clear existing operation cards
        for widget in self.content_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget not in [self.nav_frame]:
                widget.destroy()

        # Calculate start and end indices for current page
        start_idx = self.current_page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        current_operations = self.operations[start_idx:end_idx]

        # Create operation cards for current page
        for i, op in enumerate(current_operations):
            self.create_operation_card(
                self.content_frame,
                op["title"],
                op["description"],
                op["icon"],
                i // 2,
                i % 2
            )

        # Update navigation buttons and page indicator
        total_pages = (len(self.operations) + self.items_per_page - 1) // self.items_per_page
        self.page_indicator.configure(text=f"Page {self.current_page + 1}/{total_pages}")
        self.prev_button.configure(state="normal" if self.current_page > 0 else "disabled")
        self.next_button.configure(state="normal" if end_idx < len(self.operations) else "disabled")

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_operations_display()

    def next_page(self):
        if (self.current_page + 1) * self.items_per_page < len(self.operations):
            self.current_page += 1
            self.update_operations_display()

    def create_operation_card(self, parent, title, description, icon, row, col):
        """Creates a card for each operation"""
        card = ctk.CTkFrame(parent, fg_color=("#f8fafc", "#2d3748"))
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

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
        # Check if XML file is loaded
        if not self.parent.file_path:
            messagebox.showerror("Error", "Please load an XML file first.")
            return

        try:
            if operation == "Convert to JSON":
                # Ensure XML content is loaded
                if not self.parent.xml_content:
                    with open(self.parent.file_path, 'r') as file:
                        self.parent.xml_content = file.read()

                # Generate output file path (temporary)
                output_file = os.path.splitext(self.parent.file_path)[0] + ".json"

                # Create converter and convert file
                converter = XMLToJSONConverter(self.parent.file_path)
                converter.convert(output_file)

                # Read the converted JSON
                with open(output_file, 'r') as file:
                    json_content = json.dumps(json.load(file), indent=4)

                # Update OutputFrame's text box with JSON content
                output_frame = self.parent.frames['OutputFrame']
                output_frame.output_text.delete('1.0', ctk.END)
                output_frame.output_text.insert(ctk.END, json_content)

                # Update status label
                output_frame.status_label.configure(
                    text="XML Converted to JSON",
                    text_color="#10b981"
                )

                # Navigate to OutputFrame
                self.parent.show_frame("OutputFrame")
                os.remove(output_file)

            elif operation == "Minify XML":
                output_file = os.path.splitext(self.parent.file_path)[0] + "_minified.xml"

                minifier = XMLMinifier(self.parent.file_path)
                minifier.minify(output_file)

                # Read the minified XML
                with open(output_file, 'r') as file:
                    minified_content = file.read()

                # Update OutputFrame
                output_frame = self.parent.frames['OutputFrame']
                output_frame.output_text.delete('1.0', ctk.END)
                output_frame.output_text.insert(ctk.END, minified_content)

                output_frame.status_label.configure(
                    text="XML Minified Successfully",
                    text_color="#10b981"  # Success green color
                )

                # Navigate to OutputFrame
                self.parent.show_frame("OutputFrame")
                os.remove(output_file)

            elif operation == "Compress Data":
                output_file = os.path.splitext(self.parent.file_path)[0] + "_Compress.xml"

                compressor = XMLCompressor(self.parent.file_path)
                compressor.compress(output_file)

                # Read the compress Data XML
                with open(output_file, 'r') as file:
                    compressed_content = file.read()

                # Update OutputFrame
                output_frame = self.parent.frames['OutputFrame']
                output_frame.output_text.delete('1.0', ctk.END)
                output_frame.output_text.insert(ctk.END, compressed_content)

                output_frame.status_label.configure(
                    text="XML compressed Successfully",
                    text_color="#10b981"  # Success green color
                )

                # Navigate to OutputFrame
                self.parent.show_frame("OutputFrame")
                os.remove(output_file)

            elif operation == "Decompress Data":
                output_file = os.path.splitext(self.parent.file_path)[0] + "_Decompress.xml"

                decompressor = XMLDecompressor(self.parent.file_path)
                decompressor.decompress(output_file)

                # Read the decompress Data XML
                with open(output_file, 'r') as file:
                    decompressed_content = file.read()

                # Update OutputFrame
                output_frame = self.parent.frames['OutputFrame']
                output_frame.output_text.delete('1.0', ctk.END)
                output_frame.output_text.insert(ctk.END, decompressed_content)

                output_frame.status_label.configure(
                    text="XML decompressed Successfully",
                    text_color="#10b981"  # Success green color
                )

                # Navigate to OutputFrame
                self.parent.show_frame("OutputFrame")
                os.remove(output_file)

            elif operation == "Format XML":
                output_file = os.path.splitext(self.parent.file_path)[0] + "_Format.xml"

                xml_formatter = XMLFormatter(self.parent.file_path)
                xml_formatter.prettify(output_file)

                # Read the Format XML
                with open(output_file, 'r') as file:
                    formatter = file.read()

                # Update OutputFrame
                output_frame = self.parent.frames['OutputFrame']
                output_frame.output_text.delete('1.0', ctk.END)
                output_frame.output_text.insert(ctk.END, formatter)

                output_frame.status_label.configure(
                    text="XML formatteded Successfully",
                    text_color="#10b981"  # Success green color
                )

                # Navigate to OutputFrame
                self.parent.show_frame("OutputFrame")
                os.remove(output_file)

            elif operation == "Check XML Consistency":
                output_file = os.path.splitext(self.parent.file_path)[0] + "_parser.xml"

                parser = XMLParser(self.parent.file_path)
                error_count = parser.check_consistency()

                # Display errors
                if error_count > 0:
                    messagebox.showerror("Found", f"{error_count} errors")
                    parser.fix_errors()
                    fixed_file_path = os.path.splitext(self.parent.file_path)[0] + "_fixed.xml"
                    with open(fixed_file_path, 'r', encoding='utf-8') as file:
                        parsered_content = file.read()
                else:
                    messagebox.showinfo("XML Status", "XML is valid!")
                    with open(self.parent.file_path, 'r', encoding='utf-8') as file:
                        parsered_content = file.read()

                # Update OutputFrame
                output_frame = self.parent.frames['OutputFrame']
                output_frame.output_text.delete('1.0', ctk.END)
                output_frame.output_text.insert(ctk.END, parsered_content)

                output_frame.status_label.configure(
                    text="The XML file was parsed successfully",
                    text_color="#10b981"  # Success green color
                )

                # Navigate to OutputFrame
                self.parent.show_frame("OutputFrame")


            elif operation == "Draw Graph":
                try:
                    graph = GraphRepresentation.build_graph(self.parent.file_path)
                    G = nx.DiGraph()

                    # Add edges from graph representation
                    for edge in graph.edges:
                        G.add_edge(edge[0], edge[1])

                    visualizer = GraphVisualizer(G)

                    output_frame = self.parent.frames['OutputFrame']
                    output_frame.output_text.delete('1.0', ctk.END)

                    # Save visualization to a temp file first
                    temp_dir = os.path.dirname(self.parent.file_path)
                    temp_graph_path = os.path.join(temp_dir, "temp_graph.png")
                    visualizer.visualize(save_path=temp_graph_path)

                    # Show the path in output frame
                    output_frame.output_text.insert(ctk.END, f"Graph visualization saved as: {temp_graph_path}")

                    output_frame.status_label.configure(
                        text="Graph Generated Successfully",
                        text_color="#10b981"
                    )

                    self.parent.show_frame("OutputFrame")

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to generate graph: {str(e)}")

            elif operation == "Most Active User":     # can't be tested yet
                graph = GraphRepresentation.build_graph(self.parent.file_path)
                analyzer = NetworkAnalysis(graph)

                most_active_id = analyzer.get_most_active_user()
                most_active_user = graph.get_user(most_active_id)

                output_content = f"""Most Active User Analysis:

                User ID: {most_active_user.id}
                Name: {most_active_user.name}
                Number of Followers: {len(most_active_user.followers)}
                Number of Posts: {len(most_active_user.posts)}

                Posts:
                """

                for post in most_active_user.posts:
                    output_content += f"\nPost Body: {post.body}\nTopics: {', '.join(post.topics)}\n"

                # Update OutputFrame
                output_frame = self.parent.frames['OutputFrame']
                output_frame.output_text.delete('1.0', ctk.END)
                output_frame.output_text.insert(ctk.END, output_content)

                output_frame.status_label.configure(
                    text="Most Active User Found Successfully",
                    text_color="#10b981"
                )

                # Navigate to OutputFrame
                self.parent.show_frame("OutputFrame")

            elif operation == "Top Influencer":     # can't be tested yet
                # Create graph and analysis objects
                graph = GraphRepresentation.build_graph(self.parent.file_path)
                analyzer = NetworkAnalysis(graph)

                # Get top influencer
                influencer_id = analyzer.get_most_influencer_user()
                influencer = graph.get_user(influencer_id)

                # Prepare output content
                output_content = f"""Top Influencer Analysis:

                User ID: {influencer.id}
                Name: {influencer.name}
                Number of Followers: {len(influencer.followers)}
                Number of Posts: {len(influencer.posts)}

                Influence Metrics:
                - Direct Followers: {len(influencer.followers)}
                - Total Posts: {len(influencer.posts)}
                - Average Topics per Post: {sum(len(post.topics) for post in influencer.posts) / len(influencer.posts) if influencer.posts else 0:.2f}

                Recent Posts:
                """

                for post in influencer.posts[-5:]:  # Show last 5 posts
                    output_content += f"\nPost Body: {post.body}\nTopics: {', '.join(post.topics)}\n"

                # Update OutputFrame
                output_frame = self.parent.frames['OutputFrame']
                output_frame.output_text.delete('1.0', ctk.END)
                output_frame.output_text.insert(ctk.END, output_content)

                output_frame.status_label.configure(
                    text="Top Influencer Found Successfully",
                    text_color="#10b981"
                )

                # Navigate to OutputFrame
                self.parent.show_frame("OutputFrame")

            elif operation == "Mutual Users":
                # Create dialog to get user IDs
                dialog = ctk.CTkInputDialog(
                    text="Enter user IDs (comma-separated):",
                    title="Mutual Users"
                )
                user_ids_str = dialog.get_input()

                if user_ids_str:
                    try:
                        # Parse user IDs
                        user_ids = [int(id.strip()) for id in user_ids_str.split(",")]

                        # Create graph and analysis objects
                        graph = GraphRepresentation.build_graph(self.parent.file_path)
                        analyzer = NetworkAnalysis(graph)

                        # Get mutual users
                        mutual_users = analyzer.get_mutual_users(user_ids)

                        # Prepare output content
                        output_content = f"""Mutual Users Analysis:

                Input User IDs: {', '.join(map(str, user_ids))}
                Number of Mutual Users Found: {len(mutual_users)}

                Mutual Users:
                """

                        for user_id in mutual_users:
                            user = graph.get_user(user_id)
                            output_content += f"\nUser ID: {user.id}\nName: {user.name}\nFollowers: {len(user.followers)}\n"

                        # Update OutputFrame
                        output_frame = self.parent.frames['OutputFrame']
                        output_frame.output_text.delete('1.0', ctk.END)
                        output_frame.output_text.insert(ctk.END, output_content)

                        output_frame.status_label.configure(
                            text="Mutual Users Found Successfully",
                            text_color="#10b981"
                        )

                        # Navigate to OutputFrame
                        self.parent.show_frame("OutputFrame")

                    except ValueError:
                        messagebox.showerror("Error", "Please enter valid numeric user IDs")

            elif operation == "User Suggestions":
                # Create dialog to get user ID
                dialog = ctk.CTkInputDialog(
                    text="Enter user ID:",
                    title="User Suggestions"
                )
                user_id_str = dialog.get_input()

                if user_id_str:
                    try:
                        # Parse user ID
                        user_id = int(user_id_str)

                        # Create graph and analysis objects
                        graph = GraphRepresentation.build_graph(self.parent.file_path)
                        analyzer = NetworkAnalysis(graph)

                        # Get suggested users
                        suggested_users = analyzer.get_suggested_users(user_id)

                        # Prepare output content
                        output_content = f"""User Suggestions Analysis:

                For User ID: {user_id}
                Name: {graph.get_user(user_id).name}
                Number of Suggestions: {len(suggested_users)}

                Suggested Users (in order of relevance):
                """

                        for suggested_id in suggested_users[:10]:  # Show top 10 suggestions
                            user = graph.get_user(suggested_id)
                            mutual_users = analyzer.get_mutual_users([user_id, suggested_id])
                            output_content += f"\nUser ID: {user.id}"
                            output_content += f"\nName: {user.name}"
                            output_content += f"\nMutual Connections: {len(mutual_users)}"
                            output_content += f"\nTotal Followers: {len(user.followers)}\n"

                        # Update OutputFrame
                        output_frame = self.parent.frames['OutputFrame']
                        output_frame.output_text.delete('1.0', ctk.END)
                        output_frame.output_text.insert(ctk.END, output_content)

                        output_frame.status_label.configure(
                            text="User Suggestions Generated Successfully",
                            text_color="#10b981"
                        )

                        # Navigate to OutputFrame
                        self.parent.show_frame("OutputFrame")

                    except ValueError:
                        messagebox.showerror("Error", "Please enter a valid numeric user ID")

            elif operation == "Word Search":
                dialog = ctk.CTkInputDialog(
                    text="Enter word to search:",
                    title="Word Search"
                )
                search_word = dialog.get_input()
                if search_word:
                    try:
                        post_searcher = PostSearch(self.parent.file_path)
                        matching_posts = post_searcher.search_word(search_word)

                        # Prepare output content
                        output_content = f"""Word Search Results:
            Search Term: "{search_word}"
            Found in {len(matching_posts)} posts
            Matching Posts:
            """
                        for post in matching_posts:
                            output_content += f"\nPost Content: {post}\n"

                        # Update OutputFrame
                        output_frame = self.parent.frames['OutputFrame']
                        output_frame.output_text.delete('1.0', ctk.END)
                        output_frame.output_text.insert(ctk.END, output_content)

                        output_frame.status_label.configure(
                            text="Word Search Completed Successfully",
                            text_color="#10b981"
                        )

                        self.parent.show_frame("OutputFrame")

                    except Exception as e:
                        messagebox.showerror("Error", f"Search failed: {str(e)}")

            elif operation == "Topic Search":
                dialog = ctk.CTkInputDialog(
                    text="Enter topic to search:",
                    title="Topic Search"
                )

                search_topic = dialog.get_input()
                if search_topic:
                    try:
                        post_searcher = PostSearch(self.parent.file_path)
                        matching_posts = post_searcher.search_topic(search_topic)

                        # Prepare output content
                        output_content = f"""Topic Search Results:
            Search Topic: "{search_topic}"
            Found in {len(matching_posts)} posts
            Matching Posts:
            """
                        for post in matching_posts:
                            output_content += f"\nPost Content: {post}\n"

                        # Update OutputFrame
                        output_frame = self.parent.frames['OutputFrame']
                        output_frame.output_text.delete('1.0', ctk.END)
                        output_frame.output_text.insert(ctk.END, output_content)

                        output_frame.status_label.configure(
                            text="Topic Search Completed Successfully",
                            text_color="#10b981"
                        )

                        # Navigate to OutputFrame
                        self.parent.show_frame("OutputFrame")

                    except Exception as e:
                        messagebox.showerror("Error", f"Search failed: {str(e)}")
            else:
                # Placeholder for other operations
                messagebox.showinfo("Operation", f"{operation} is not yet implemented.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")