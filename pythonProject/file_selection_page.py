import tkinter as tk
from tkinter import ttk
import os
from datetime import datetime
from config import FILE_TYPES
from tkinter import messagebox
import pandas as pd
import re
import openpyxl

class FileSelectionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.item_id_to_full_path = {}
        self.folder_path = ""
        self.selected_file_type = ""
        self.selection_state = {}  # Maps item IDs to their selection state
        self.selected_file_type = tk.StringVar(value=FILE_TYPES[0])
        self.combobox = ttk.Combobox(self, textvariable=self.selected_file_type, values=FILE_TYPES, state='readonly')
        self.combobox.grid(row=1, column=1, padx=10, pady=10, sticky="e")
        self.combobox.bind("<<ComboboxSelected>>", self.on_file_type_change)

        # Corrected Treeview setup for displaying file names
        self.file_tree = ttk.Treeview(self, columns=("file_name", "size", "last_modified", "selected"), show="headings",
                                      selectmode="extended")
        self.file_tree.heading("file_name", text="File Name")
        self.file_tree.heading("size", text="Size (KB)")
        self.file_tree.heading("last_modified", text="Last Modified")
        self.file_tree.heading("selected", text="Select")
        self.file_tree.column("file_name", anchor="w", width=300)
        self.file_tree.column("size", anchor="center", width=90)
        self.file_tree.column("last_modified", anchor="center", width=115)
        self.file_tree.column("selected", anchor="center", width=55)
        self.file_tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew",
                            columnspan=2)  # Ensure columnspan accommodates the scrollbar

        self.file_tree.bind("<<TreeviewSelect>>", self.update_selection_state)

        # Scrollbar setup
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.file_tree.yview)
        self.file_tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=2, sticky='ns')  # Adjusted to use grid

        # Button setup
        tk.Button(self, text="Select All", command=self.select_all).grid(row=1, column=0, padx=10, pady=2, sticky="ew")
        tk.Button(self, text="Deselect All", command=self.deselect_all).grid(row=2, column=0, padx=10, pady=2,
                                                                             sticky="ew")
        tk.Button(self, text="Next", command=self.show_selected_files).grid(row=3, column=0, padx=10, pady=10,
                                                                            sticky="ew")
        tk.Button(self, text="Back to Folder Selection",
                  command=lambda: controller.show_page("FolderSelectionPage")).grid(row=4, column=0, padx=10, pady=2,
                                                                                    sticky="ew")

        # Add a label and entry for row skipping
        tk.Label(self, text="Skip Rows:").grid(row=3, column=1, padx=80, pady=10, sticky="w")
        self.skip_rows_var = tk.StringVar(value="0")
        self.skip_rows_entry = tk.Entry(self, textvariable=self.skip_rows_var, validate='key', validatecommand=(self.register(self.validate_numeric), '%P'))
        self.skip_rows_entry.grid(row=3, column=1, padx=10, pady=10, sticky="e")

        # Add a checkbox for sampling option
        self.sample_var = tk.BooleanVar(value=False)
        self.sample_checkbox = tk.Checkbutton(self, text="Sample Data (20000 rows)", variable=self.sample_var)
        self.sample_checkbox.grid(row=2, column=1, padx=10, pady=2, sticky="e")

        parent.rowconfigure(0, weight=1)  # Allow this row to expand
        parent.columnconfigure(0, weight=1)  # Allow this column to expand
        # Bind the left mouse click to a new method
        self.file_tree.bind("<Button-1>", self.on_item_click, add="+")

    def validate_numeric(self, new_value):
        """Validate that only numeric input is allowed."""
        return new_value.isdigit() or new_value == ""

    def on_item_click(self, event):
        """Handles toggling selection state of an item when it is clicked."""
        item = self.file_tree.identify_row(event.y)
        if not item:
            return  # Exit if the click was not on an item

        column = self.file_tree.identify_column(event.x)
        if self.file_tree.heading(column, "text") == "Select":
            return  # Exit if the 'Select' column was clicked

        if item:
            if item in self.file_tree.selection():
                self.file_tree.selection_remove(item)
                self.selection_state[item] = False
            else:
                self.file_tree.selection_add(item)
                self.selection_state[item] = True
            self.update_selection_state()

        return "break"

    def update_file_tree(self):
        self.file_tree.delete(*self.file_tree.get_children())  # Clear existing entries
        file_type = self.selected_file_type.get()
        if os.path.isdir(self.folder_path):
            for file in os.listdir(self.folder_path):
                if file.endswith(file_type):
                    full_path = os.path.join(self.folder_path, file)  # Get full path
                    full_path = os.path.normpath(full_path)
                    print(full_path)
                    size_bytes = os.path.getsize(full_path)
                    size_kb = size_bytes / 1024  # Convert bytes to KB
                    size = "{:.2f} KB".format(size_kb)
                    last_modified = datetime.fromtimestamp(os.path.getmtime(full_path)).strftime('%Y-%m-%d %H:%M:%S')
                    self.selection_state[full_path] = False
                    # Insert file with name and attach full_path as part of the item's values or tags
                    item_id = self.file_tree.insert("", tk.END, values=(file, size, last_modified))
                    # Store the full path in the item's tag for easy retrieval
                    self.item_id_to_full_path[item_id] = full_path  # Store the mapping
        self.refresh_treeview_selection()

    def update_selection_state(self, event=None):
        selected_items = self.file_tree.selection()
        for item in self.file_tree.get_children():
            if item in selected_items:
                self.file_tree.set(item, "selected", "✓")
            else:
                self.file_tree.set(item, "selected", "")

    def select_all(self):
        """Select all items, visually and internally."""
        for item in self.file_tree.get_children():
            self.selection_state[item] = True
            self.file_tree.selection_add(item)  # Add item to Treeview's selection
        self.refresh_treeview_selection()

    def deselect_all(self):
        """Deselect all items, visually and internally."""
        for item in self.file_tree.get_children():
            self.selection_state[item] = False
            self.file_tree.selection_remove(item)  # Remove item from Treeview's selection
        self.refresh_treeview_selection()

    def show_selected_files(self):
        if self.check_file_structure():
            selected_files = self.get_selected_files()
            skip_rows = int(self.skip_rows_var.get() or 0)
            sample_data = self.sample_var.get()
            self.controller.show_selected_files_page(selected_files, skip_rows, sample_data)  # Proceed to next page

    def get_selected_files(self):
        selected_items = self.file_tree.selection()
        selected_files_full_path = []
        for item_id in selected_items:
            if item_id in self.item_id_to_full_path:
                selected_files_full_path.append(self.item_id_to_full_path[item_id])
            else:
                print(f"Missing item ID in dictionary: {item_id}")  # For debugging
        return selected_files_full_path

    def update_with_new_folder(self, folder_path):
        self.folder_path = folder_path
        # Add any additional logic needed to refresh or update the page based on the new folder path
        self.update_file_tree()

    def refresh_treeview_selection(self):
        """Synchronize the visual ticks with the current Treeview selection."""
        selected_items = self.file_tree.selection()
        for item in self.file_tree.get_children():
            # Set the tick mark for selected items
            if item in selected_items:
                self.file_tree.set(item, "selected", "✓")
            else:
                self.file_tree.set(item, "selected", "")

    def toggle_selection(self):
        """Toggle selection state for the selected item(s) and refresh the Treeview."""
        for item in self.file_tree.selection():
            # Toggle the selection state
            is_selected = self.selection_state.get(item, False)
            self.selection_state[item] = not is_selected

        # Refresh the Treeview to reflect the updated selection states
        self.refresh_treeview_selection()

    def on_file_type_change(self, event=None):  # Include the event parameter
        # Code to handle the combobox selection change
        self.update_file_tree()

    def check_file_structure(self):
        selected_files = self.get_selected_files()
        file_details = {}  # Dictionary to hold file name (normalized) and size
        base_header = None  # Initialize base_header outside the loop

        for file_path in selected_files:
            file_size = os.path.getsize(file_path)
            # Normalize file name (e.g., remove patterns like ' (1)' and file extension)
            file_name_normalized = re.sub(r' \(\d+\)|\.\w+$', '', os.path.basename(file_path))

            # Check for potential duplicates based on normalized name and size
            if file_name_normalized in file_details and file_details[file_name_normalized]['size'] == file_size:
                messagebox.showerror("Error",
                                     f"Duplicate files detected based on name and size: {file_path} and {file_details[file_name_normalized]['path']}")
                return False

            file_details[file_name_normalized] = {'size': file_size,
                                                  'path': file_path}  # Record file details for later reference

            try:
                # Determine the file type and read the header accordingly
                if file_path.endswith('.csv'):
                    skip_rows = int(self.skip_rows_var.get() or 0)
                    data = pd.read_csv(file_path, nrows=20000 if self.sample_var.get() else None, skiprows=skip_rows, low_memory=False)  # For CSV files
                elif file_path.endswith('.txt'):
                    skip_rows = int(self.skip_rows_var.get() or 0)
                    data = pd.read_csv(file_path, delimiter='\t', nrows=20000 if self.sample_var.get() else None, skiprows=skip_rows, low_memory=False)  # For TXT files, assuming tab-delimited
                elif file_path.endswith('.xlsx'):
                    skip_rows = int(self.skip_rows_var.get() or 0)
                    data = pd.read_excel(file_path, nrows=20000 if self.sample_var.get() else None, skiprows=skip_rows)  # For Excel files
                else:
                    messagebox.showwarning("Warning", f"Unsupported file type: {file_path}")
                    continue  # Skip unsupported file types

                current_header = data.columns.tolist()

                # Check if the header is empty
                if not current_header:
                    messagebox.showwarning("Warning", f"The file {file_path} has an empty header and will be skipped.")
                    continue

                if base_header is None:
                    base_header = current_header
                elif base_header != current_header:
                    messagebox.showerror("Error", "The files you selected do not share the same structure.")
                    return False  # If the current header does not match the base header, return False

            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file {file_path}: {e}")
                return False

        return True  # If all non-empty headers match, and no duplicates found, return True
