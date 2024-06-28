import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image, ImageTk
import pandas as pd


class DisplaySelectedInfoPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.group_mode = tk.BooleanVar(value=False)  # Pre-set to Split
        self.imageDir = os.path.dirname(__file__)  # Assuming images are in the same directory as the script
        self.layout_widgets()
        self.selected_files = []
        self.selected_unique_items = []
        self.selected_items_count = 0
        self.combined_data = pd.DataFrame()
        self.disable_selection()
        self.on_toggle()  # Set the initial state based on the default mode

    def load_image(self, file_name, size=(60, 30)):
        image_path = os.path.join(self.imageDir, file_name)
        image = Image.open(image_path)
        image = image.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    def layout_widgets(self):
        # Load images
        self.toggle_off = self.load_image('Image/off.png')
        self.toggle_on = self.load_image('Image/on.png')

        # Create custom style
        style = ttk.Style()
        style.element_create("Checkbutton.toggle", "image", self.toggle_off,
                             ("selected", self.toggle_on), border=8, sticky="w")
        style.layout("TCheckbutton.Toggle.Green",
                     [("Checkbutton.padding",
                       {"sticky": "nswe", "children": [("Checkbutton.toggle", {"side": "left", "sticky": ""}),
                                                       ("Checkbutton.label", {"sticky": "nswe"})]})])

        # Create the grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)

        # Add search bar and button
        self.search_frame = tk.Frame(self)
        self.search_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.search_var = tk.StringVar()
        self.search_bar = tk.Entry(self.search_frame, textvariable=self.search_var, width=30)
        self.search_bar.pack(side="right", padx=5, pady=5)

        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_items)
        self.search_button.pack(side="right", padx=5, pady=5)

        self.txt_files = tk.Text(self, height=5, wrap="word", width=40, font=("Arial", 10), state='disabled')
        self.txt_files.grid(row=1, column=0, padx=5, pady=5, sticky="nw")

        self.lbl_file_count = tk.Label(self, text="File Count: 0")
        self.lbl_file_count.grid(row=2, column=0, padx=5, pady=0, sticky="nw")

        self.lbl_header = tk.Label(self, text="Selected Header:")
        self.lbl_header.grid(row=3, column=0, padx=5, pady=15, sticky="nw")

        self.txt_header = tk.Text(self, height=1, wrap="word", width=40, font=("Arial", 10), state='disabled')
        self.txt_header.grid(row=3, column=0, padx=5, pady=30, sticky="w")

        self.lbl_unique_item_count = tk.Label(self, text="Unique Items Count: 0")
        self.lbl_unique_item_count.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.lbl_row_skip_count = tk.Label(self, text="Rows Skipped: 0")
        self.lbl_row_skip_count.grid(row=2, column=0, padx=5, pady=0, sticky="sw")

        # Add a label for displaying the count of selected items
        self.lbl_selected_item_count = tk.Label(self, text="Selected Items Count: 0")
        self.lbl_selected_item_count.grid(row=3, column=0, padx=5, pady=0, sticky="sw")

        self.lst_unique_items = ttk.Treeview(self, columns=("item", "selected"), show="headings", height=10)
        self.lst_unique_items.heading("item", text="Item")
        self.lst_unique_items.heading("selected", text="Selected")
        self.lst_unique_items.column("item", width=150)
        self.lst_unique_items.column("selected", width=50)
        self.lst_unique_items.grid(row=1, column=1, rowspan=5, padx=5, pady=5, sticky="nsew")

        # Container for buttons
        button_container = tk.Frame(self)
        button_container.grid(row=6, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

        # Extract button
        extract_button = tk.Button(button_container, text="Next", command=self.extract_action)
        extract_button.pack(side="right", padx=5)

        # Back button to return to the previous page
        back_button = tk.Button(button_container, text="Back",
                                command=lambda: self.controller.show_page("SelectedFilesPage"))
        back_button.pack(side="right", padx=5)

        # Toggle button for Split/Group
        self.toggle_button = ttk.Checkbutton(button_container, style="TCheckbutton.Toggle.Green",
                                             variable=self.group_mode, command=self.on_toggle)
        self.toggle_button.pack(side="left", padx=5)

        self.lbl_group = tk.Label(button_container, text="Current Option: Split")
        self.lbl_group.pack(side="left")

    def display_selected_info(self, files, header, unique_items, skip_rows, combined_data):
        self.txt_files.config(state='normal')
        self.txt_files.delete('1.0', tk.END)
        file_names = [os.path.basename(f) for f in files]
        self.txt_files.insert(tk.END, "\n".join(file_names))
        self.txt_files.config(state='disabled')

        self.txt_header.config(state='normal')
        self.txt_header.delete('1.0', tk.END)
        self.txt_header.insert(tk.END, header)
        self.txt_header.config(state='disabled')

        self.lbl_file_count.config(text=f"File Count: {len(files)}")
        self.lbl_unique_item_count.config(text=f"Unique Items Count: {len(unique_items)}")
        self.lbl_row_skip_count.config(text=f"Rows Skipped: {skip_rows}")

        self.lst_unique_items.delete(*self.lst_unique_items.get_children())
        for item in unique_items:
            self.lst_unique_items.insert('', tk.END, values=(item, '✓' if not self.group_mode.get() else ''))

        # Update selected files and unique items for further processing
        self.selected_files = files
        self.selected_unique_items = unique_items
        self.combined_data = combined_data

        # Update selected items count based on the current mode
        self.update_selected_item_count()

    def on_toggle(self):
        if self.group_mode.get():
            self.enable_selection()
            self.lbl_group.config(text="Current Option: Group")
            self.search_bar.config(state='normal')
            self.search_button.config(state='normal')
        else:
            self.disable_selection()
            self.lbl_group.config(text="Current Option: Split")
            self.search_bar.config(state='disabled')
            self.search_button.config(state='disabled')

        # Update selected items count based on the current mode
        self.update_selected_item_count()

    def enable_selection(self):
        for child in self.lst_unique_items.get_children():
            self.lst_unique_items.item(child, values=(self.lst_unique_items.item(child, "values")[0], ''))
        self.lst_unique_items.bind('<ButtonRelease-1>', self.toggle_selected)

    def disable_selection(self):
        self.lst_unique_items.unbind('<ButtonRelease-1>')
        for child in self.lst_unique_items.get_children():
            self.lst_unique_items.item(child, values=(self.lst_unique_items.item(child, "values")[0], '✓'))

    def toggle_selected(self, event):
        selected_item = self.lst_unique_items.focus()
        if selected_item:
            current_value = self.lst_unique_items.item(selected_item, "values")[1]
            new_value = '✓' if current_value == '' else ''
            self.lst_unique_items.item(selected_item,
                                       values=(self.lst_unique_items.item(selected_item, "values")[0], new_value))
            # Update the count of selected unique items
            self.update_selected_item_count()

    def search_items(self):
        if self.group_mode.get():
            search_term = self.search_var.get().lower()
            conditions = search_term.split(';')
            include_conditions = [cond for cond in conditions if not cond.startswith('!')]
            exclude_conditions = [cond[1:] for cond in conditions if cond.startswith('!')]

            for child in self.lst_unique_items.get_children():
                item_value = self.lst_unique_items.item(child, "values")[0]
                item_lower = item_value.lower()
                include = all(cond in item_lower for cond in include_conditions)
                exclude = any(cond in item_lower for cond in exclude_conditions)

                if include and not exclude:
                    self.lst_unique_items.item(child, values=(item_value, '✓'))
                else:
                    self.lst_unique_items.item(child, values=(item_value, ''))

            # Update the count of selected unique items
            self.update_selected_item_count()

    def update_selected_item_count(self):
        if self.group_mode.get():
            selected_count = len([item for item in self.lst_unique_items.get_children()
                                  if self.lst_unique_items.item(item, "values")[1] == '✓'])
        else:
            selected_count = len(self.selected_unique_items)

        self.selected_items_count = selected_count
        self.lbl_selected_item_count.config(text=f"Selected Items Count: {selected_count}")

    def extract_action(self):
        if self.group_mode.get() and self.selected_items_count == 0:
            messagebox.showerror("Selection Error", "No items selected. Please select at least one item.")
        else:
            popup = PopupDialog(self)
            self.wait_window(popup.top)
            if popup.result:
                output_path, output_name, output_type = popup.result
                print(f"Output Path: {output_path}")
                print(f"Output Name: {output_name}")
                print(f"Output Type: {output_type}")

                # Implementing file generation based on the user input
                self.generate_output(output_path, output_name, output_type)

    def generate_output(self, output_path, output_name, output_type):
        if not os.path.exists(output_path):
            messagebox.showerror("Path Error", "The specified output path does not exist.")
            return

        if self.group_mode.get():
            # Group mode: Generate a single file with selected items
            selected_items = [self.lst_unique_items.item(item, "values")[0] for item in
                              self.lst_unique_items.get_children()
                              if self.lst_unique_items.item(item, "values")[1] == '✓']
            print(f"Selected items for group mode: {selected_items}")
            filtered_data = self.combined_data[
                self.combined_data[self.txt_header.get("1.0", "end-1c")].isin(selected_items)]
            print(f"Filtered data: {filtered_data}")
            output_file = os.path.join(output_path, f"{output_name}.{output_type}")
            self.save_to_file(filtered_data, output_file, output_type)
        else:
            # Split mode: Generate separate files for each unique item
            header = self.txt_header.get("1.0", "end-1c")
            for item in self.selected_unique_items:
                filtered_data = self.combined_data[self.combined_data[header] == item]
                output_file = os.path.join(output_path, f"{output_name}_{item}.{output_type}")
                self.save_to_file(filtered_data, output_file, output_type)

        messagebox.showinfo("Success", "Files generated successfully.")

    def save_to_file(self, data, file_path, file_type):
        try:
            if file_type == "csv":
                data.to_csv(file_path, index=False)
            elif file_type == "xlsx":
                data.to_excel(file_path, index=False)
            elif file_type == "txt":
                data.to_csv(file_path, index=False, sep='\t')
            elif file_type == "pdf":
                # Implement PDF export functionality as needed
                pass
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save file: {e}")


class PopupDialog:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        self.result = None
        self.parent = parent
        self.group_mode = parent.group_mode.get()

        top.grab_set()  # Lock the main window
        top.transient(parent)  # Always on top
        top.title("Select Output Options")
        top.resizable(False, False)  # Prevent resizing

        # Set the desired size of the pop-up window
        self.set_size(top, width=450, height=150)  # Adjust width and height as needed
        # Center the pop-up window relative to the main window
        self.center_window(top, parent)

        tk.Label(top, text="Select Output Path").grid(row=0, column=0, padx=5, pady=5)
        self.path_entry = tk.Entry(top, width=40)
        self.path_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(top, text="Browse", command=self.browse_path).grid(row=0, column=2, padx=5, pady=5)

        if self.group_mode:
            tk.Label(top, text="File Name").grid(row=1, column=0, padx=5, pady=5)
        else:
            tk.Label(top, text="Root Name").grid(row=1, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(top, width=40)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(top, text="Select Output Type").grid(row=2, column=0, padx=5, pady=5)
        self.output_type = ttk.Combobox(top, values=["csv", "txt", "xlsx", "pdf"])
        self.output_type.grid(row=2, column=1, padx=5, pady=5)
        self.output_type.current(0)  # set default to first option

        tk.Button(top, text="Extract", command=self.on_ok).grid(row=3, column=1, padx=5, pady=5)

    def browse_path(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.insert(0, directory)

    def on_ok(self):
        output_path = self.path_entry.get()
        output_name = self.name_entry.get()
        output_type = self.output_type.get()

        if output_path and output_name and output_type:
            self.result = (output_path, output_name, output_type)
            self.top.destroy()
        else:
            messagebox.showerror("Input Error", "All fields must be filled out.")

    def set_size(self, top, width, height):
        top.geometry(f'{width}x{height}')

    def center_window(self, top, parent):
        top.update_idletasks()

        # Get the dimensions of the main window
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        # Get the dimensions of the pop-up window
        top_width = top.winfo_width()
        top_height = top.winfo_height()

        # Calculate position to center the pop-up window in the main window
        x = parent_x + (parent_width // 2) - (top_width // 2)
        y = parent_y + (parent_height // 2) - (top_height // 2)

        top.geometry(f'{top_width}x{top_height}+{x}+{y}')
