import tkinter as tk
from tkinter import ttk  # For Combobox
from tkinter import filedialog
import os


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Handler")
        self.geometry("600x400")

        self.page_number = 0
        self.selected_folder = ""
        self.file_types = ['.xlsx', '.csv', '.txt']

        self.folder_path = tk.StringVar()
        self.text_box = tk.Entry(self, textvariable=self.folder_path)
        self.select_folder_btn = tk.Button(self, text="Select Folder", command=self.select_folder)

        # Dropdown for file type selection
        self.file_type_var = tk.StringVar()
        self.file_type_dropdown = ttk.Combobox(self, textvariable=self.file_type_var, values=self.file_types + ['all'],
                                               state='readonly')
        self.file_type_dropdown.set('all')
        self.file_type_dropdown.bind('<<ComboboxSelected>>', lambda e: self.update_file_list())

        # Adjusting font size for Listbox
        self.file_listbox = tk.Listbox(self, selectmode='extended', exportselection=0, font=('Courier', 10))

        # Buttons for selecting and deselecting all items
        self.select_all_btn = tk.Button(self, text="Select All", command=lambda: self.select_deselect_all(True))
        self.deselect_all_btn = tk.Button(self, text="Deselect All", command=lambda: self.select_deselect_all(False))

        self.previous_btn = tk.Button(self, text="Previous", command=self.go_previous)
        self.next_btn = tk.Button(self, text="Next", command=self.go_next)
        self.close_btn = tk.Button(self, text="Close", command=self.destroy)

        self.update_ui_for_page()
        self.file_listbox.bind('<<ListboxSelect>>', self.update_selection)

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.selected_folder = folder_selected
            self.folder_path.set(folder_selected)
            self.update_file_list()

    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        selected_type = self.file_type_var.get()
        if os.path.isdir(self.selected_folder):
            files = [f for f in os.listdir(self.selected_folder) if selected_type == 'all' or f.endswith(
                tuple(self.file_types) if selected_type == 'all' else selected_type)]
            max_length = max(len(file) for file in files) if files else 0
            for file in files:
                display_file = file.ljust(max_length + 4)  # Padding for tick mark
                self.file_listbox.insert(tk.END, display_file)

    def select_deselect_all(self, select_all=True):
        self.file_listbox.selection_clear(0, tk.END)
        if select_all:
            self.file_listbox.select_set(0, tk.END)
        self.update_selection()

    def update_selection(self, event=None):
        selected_indices = self.file_listbox.curselection()
        # Calculate max length considering the space for a tick for all items, even if not currently selected
        max_length = max(
            len(self.file_listbox.get(i).strip()) for i in range(self.file_listbox.size())) + 2  # +2 for tick and space

        for i in range(self.file_listbox.size()):
            item_text = self.file_listbox.get(i).strip()
            if "✓" in item_text:
                # If item already has a tick, remove it to get the original item text
                item_text = item_text[2:].strip()  # Remove the tick and the space after it

            if i in selected_indices:
                # Item is selected, add a tick mark in front
                display_text = f"✓ {item_text}".ljust(max_length)
            else:
                # Item is not selected, do not add a tick mark but reserve space
                display_text = f"  {item_text}".ljust(max_length)

            self.file_listbox.delete(i)
            self.file_listbox.insert(i, display_text)

    def go_previous(self):
        self.page_number = max(0, self.page_number - 1)
        self.update_ui_for_page()

    def go_next(self):
        self.page_number += 1
        self.update_ui_for_page()

    def update_ui_for_page(self):
        self.text_box.grid_remove()
        self.select_folder_btn.grid_remove()
        self.file_type_dropdown.grid_remove()
        self.file_listbox.grid_remove()
        self.select_all_btn.grid_remove()
        self.deselect_all_btn.grid_remove()

        if self.page_number == 0:
            self.text_box.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
            self.select_folder_btn.grid(row=0, column=1, padx=10, pady=10)
            self.file_type_dropdown.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        elif self.page_number == 1:
            self.file_listbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ewns")
            self.select_all_btn.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
            self.deselect_all_btn.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.previous_btn.grid(row=3, column=0, padx=10, pady=20, sticky="ew")
        self.next_btn.grid(row=3, column=1, padx=10, pady=20, sticky="ew")
        self.close_btn.grid(row=3, column=2, padx=10, pady=20, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


if __name__ == "__main__":
    app = Application()
    app.mainloop()