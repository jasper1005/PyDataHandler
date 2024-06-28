import tkinter as tk
from tkinter import ttk
import os
from datetime import datetime
import pandas as pd
from tkinter import messagebox

class SelectedFilesPage(tk.Frame):
    def __init__(self, parent, controller, max_unique_items=100):
        super().__init__(parent)
        self.controller = controller
        self.max_unique_items = max_unique_items  # Store the limit
        self.files = []  # Store the list of selected files
        self.selected_header = None
        self.sample_data = False  # Initialize the sample data flag
        self.unique_items_cache = {}  # Cache for unique items
        self.combined_data = pd.DataFrame()  # Initialize combined_data attribute
        self.layout_widgets()

    def layout_widgets(self):
        # Container for the Treeview, list views, and buttons
        content_frame = tk.Frame(self)
        content_frame.pack(side="top", fill="both", expand=True, padx=20, pady=20)

        # Adjust the Treeview widget setup
        self.tree = ttk.Treeview(content_frame, columns=("file_name", "size", "last_modified"), show="headings",
                                 height=8)
        self.tree.heading("file_name", text="File Name")
        self.tree.heading("size", text="Size (KB)")
        self.tree.heading("last_modified", text="Last Modified")
        self.tree.column("file_name", anchor="w", width=300)  # Adjust width as needed
        self.tree.column("size", anchor="center", width=100)
        self.tree.column("last_modified", anchor="center", width=150)
        self.tree.pack(side="top", fill="x")

        # Scrollbar setup
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", before=self.tree)

        # Frame for list views
        list_views_frame = tk.Frame(content_frame)
        list_views_frame.pack(side="top", fill="x", expand=False, pady=10)

        # Frame for headers listbox
        self.frame_headers = tk.Frame(list_views_frame)
        self.frame_headers.pack(side="left", fill="x", expand=False, padx=10)

        self.lbl_headers = tk.Label(self.frame_headers, text="Headers")
        self.lbl_headers.pack(fill="x")

        # Set the height of the Listbox to reduce its vertical size
        self.lst_headers = tk.Listbox(self.frame_headers, height=4, width=40)  # Height reduced to 4 lines
        self.lst_headers.pack(fill="x", padx=5)

        # Frame for unique items listbox
        self.frame_items = tk.Frame(list_views_frame)
        self.frame_items.pack(side="left", fill="x", expand=False, padx=10)

        self.lbl_items = tk.Label(self.frame_items, text="Unique Items")
        self.lbl_items.pack(fill="x")

        # Set the height of the Listbox to reduce its vertical size
        self.lst_items = tk.Listbox(self.frame_items, height=4, width=40)  # Height reduced to 4 lines
        self.lst_items.pack(fill="x", padx=5)

        # Container for the navigation buttons at the bottom
        button_container = tk.Frame(content_frame)
        button_container.pack(side="bottom", fill="x", pady=10)

        back_button = tk.Button(button_container, text="Back to File Selection",
                                command=lambda: self.controller.show_page("FileSelectionPage"))
        back_button.pack(side="left", padx=20)

        next_button = tk.Button(button_container, text="Next", command=self.show_selected_info)
        next_button.pack(side="right", padx=20)

        self.lst_headers.bind('<<ListboxSelect>>', self.on_header_select)

    def display_selected_files(self, files, skip_rows, sample_data):
        self.files = files  # Store the list of selected files
        self.skip_rows = skip_rows
        self.sample_data = sample_data  # Store the sample data flag
        self.unique_items_cache.clear()  # Clear the cache when displaying new files
        self.tree.delete(*self.tree.get_children())  # Clear existing entries
        for full_file_path in files:
            file_name = os.path.basename(full_file_path)
            size_bytes = os.path.getsize(full_file_path)
            size_kb = size_bytes / 1024
            size = "{:.2f} KB".format(size_kb)
            last_modified = datetime.fromtimestamp(os.path.getmtime(full_file_path)).strftime('%Y-%m-%d %H:%M:%S')
            self.tree.insert("", tk.END, values=(file_name, size, last_modified))

        if files:
            self.display_headers(files)  # Display headers for all selected files

    def on_header_select(self, event):
        selection_index = self.lst_headers.curselection()
        if not selection_index:
            return
        self.selected_header = self.lst_headers.get(selection_index[0])
        if self.selected_header.lower() in ['date', 'amount', 'id']:
            self.lst_items.delete(0, tk.END)  # Clear the listbox if selected header is date, amount, or ID
            return

        # Use cached unique items if available
        if self.selected_header in self.unique_items_cache:
            unique_items = self.unique_items_cache[self.selected_header]
        else:
            unique_items = set()  # Use a set to avoid duplicates
            try:
                combined_data = self.combined_data  # Use combined_data attribute
                unique_items.update(combined_data[self.selected_header].dropna().unique())
                self.unique_items_cache[self.selected_header] = unique_items  # Cache the unique items
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process files: {e}")
                return

        self.lst_items.delete(0, tk.END)  # Clear existing entries
        for item in unique_items:
            self.lst_items.insert(tk.END, item)

    def display_headers(self, files):
        self.lst_headers.delete(0, tk.END)  # Clear existing entries
        all_headers = set()  # Use a set to avoid duplicate headers
        try:
            self.combined_data = pd.DataFrame()  # Initialize combined_data
            for file_path in files:
                nrows = 20000 if self.sample_data else None
                data = pd.read_csv(file_path, nrows=nrows, skiprows=self.skip_rows, low_memory=False)  # Read only a few rows to get the headers
                self.combined_data = pd.concat([self.combined_data, data], ignore_index=True)

            for column in self.combined_data.columns:
                # Check if the column should be classified
                if self.is_column_for_classification(self.combined_data, column):
                    all_headers.add(column)

            for header in sorted(all_headers):  # Sort headers alphabetically for better readability
                self.lst_headers.insert(tk.END, header)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file headers: {e}")

    def is_column_for_classification(self, data, column):
        """Determine if the column is suitable for classification based on the uniqueness percentage."""
        column_data = data[column].dropna()  # Drop NA values to ensure accurate calculations
        total_count = len(column_data)  # Total non-NA items in the column

        if total_count == 0:
            print(f"Column {column} is empty.")
            return False  # If the column is empty, it's not suitable for classification

        unique_items = column_data.unique()
        unique_count = len(unique_items)  # Number of unique non-NA items

        print(f"Column {column}: Total count = {total_count}, Unique count = {unique_count}")

        if unique_count <= 50:
            print(f"Column {column} is suitable for classification: less than or equal to 50 unique items.")
            self.unique_items_cache[column] = unique_items  # Cache the unique items
            return True  # Suitable for classification if unique items are very few

        if total_count == 20000:  # Adjusted for sample size of 20000 rows
            unique_percentage = (unique_count / total_count) * 100
            print(f"Column {column}: Unique percentage = {unique_percentage}%")
            if unique_percentage <= 0.0025:
                print(f"Column {column} is suitable for classification: unique percentage <= 0.0025%.")
                self.unique_items_cache[column] = unique_items  # Cache the unique items
                return True
            else:
                print(f"Column {column} is not suitable: unique percentage > 0.0025%.")
                return False

        print(f"Column {column} does not meet any criteria for classification.")
        return False  # Default to not suitable if none of the above conditions are met

    def show_selected_info(self):
        if not self.selected_header:
            messagebox.showerror("Error", "No header selected.")
            return

        unique_items = [self.lst_items.get(i) for i in range(self.lst_items.size())]

        selected_info_page = self.controller.pages['DisplaySelectedInfoPage']
        selected_info_page.display_selected_info(self.files, self.selected_header, unique_items, self.skip_rows, self.combined_data)
        self.controller.show_page("DisplaySelectedInfoPage")