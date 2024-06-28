import tkinter as tk
from tkinter import ttk, filedialog
from config import FILE_TYPES
import os

class FolderSelectionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.folder_path = tk.StringVar()

        self.folder_path.trace("w", self.on_folder_path_change)

        # Configure the grid layout to have more columns for flexibility
        for col in range(3):
            self.columnconfigure(col, weight=1)
        self.columnconfigure(4, weight=0)  # Don't expand the last column (where buttons are)
        # Configure the grid layout to have rows with weights
        for row in range(3):
            self.rowconfigure(row, weight=1)

        # Add instructions using a Text widget to allow for bolding the header
        instructions = tk.Text(self, font=("Arial", 10), wrap="word", padx=20, pady=10, height=20)
        instructions.grid(row=0, column=0, columnspan=5, sticky="ew")
        instructions.insert(tk.END, "Instructions:\n", "header")
        instructions.insert(tk.END, (
            "- Select the folder containing your files by clicking 'Select Folder'.\n"
            "- The selected folder path will be displayed in the text field.\n"
            "- Click 'Next' to proceed to the File Selection page.\n\n"))
        instructions.insert(tk.END, "File Selection Page:\n", "header")
        instructions.insert(tk.END, (
            "- Choose the type of files you want to select from the dropdown menu.\n"
            "- Select the files you want to process. You can use 'Select All' or 'Deselect All' buttons.\n"
            "- Specify the number of rows to skip if necessary.\n"
            "- Optionally, enable 'Sample Data' to process only the first 20,000 rows.\n"
            "- Click 'Next' to proceed to the Selected Files page.\n\n"))
        instructions.insert(tk.END, "Selected Files Page:\n", "header")
        instructions.insert(tk.END, (
            "- Review the list of selected files and their details.\n"
            "- Select a header to classify unique items from the file data.\n"
            "- Click 'Next' to proceed to the Display Selected Info page.\n\n"))
        instructions.insert(tk.END, "Display Selected Info Page:\n", "header")
        instructions.insert(tk.END, (
            "- Review the unique items and select the desired items for processing.\n"
            "- Use the toggle button to switch between Split and Group modes\n"
            "- Use the search bar to filter items based on conditions.\n"
            "- Click 'Next' to proceed to the output options dialog.\n\n"))
        instructions.insert(tk.END, "Output Path Selecting Page:\n", "header")
        instructions.insert(tk.END, (
            "- Choose the output path, file name, and format.\n"
            "- Click 'Extract' to generate the output files.\n"
        ))

        # Apply the bold font to the headers
        instructions.tag_configure("header", font=("Arial", 10, "bold"))
        instructions.config(state=tk.DISABLED)  # Make the Text widget read-only

        # Entry widget spanning several columns to make it longer and placed in the center
        entry = tk.Entry(self, textvariable=self.folder_path, font=("Arial", 12))
        entry.grid(row=2, column=0, columnspan=4, sticky="ew", padx=(20, 0))
        entry.bind("<Control-v>", self.paste_from_clipboard)

        # 'Select Folder' button next to the Entry widget
        button_select_folder = tk.Button(self, text="Select Folder", command=self.select_folder, font=("Arial", 12), bg="#007BFF", fg="white")
        button_select_folder.grid(row=2, column=4, sticky="ew", padx=(10, 20))

        # 'Close' button in the second to last column, bottom row, aligned right
        button_close = tk.Button(self, text="Close", command=self.close_application, font=("Arial", 12), bg="#DC3545", fg="white")
        button_close.grid(row=3, column=0, sticky="se", padx=(0, 5), pady=10, ipadx=30)

        # 'Next' button in the last column, bottom row, aligned left
        button_next = tk.Button(self, text="Next", command=lambda: controller.show_page("FileSelectionPage"), font=("Arial", 12), bg="#28A745", fg="white")
        button_next.grid(row=3, column=4, sticky="sw", padx=(10, 0), pady=10, ipadx=30)

        # Add credit
        credit_label = tk.Label(self, text="Created by Jasper Cheng@2024", font=("Arial", 10), anchor="e", padx=20, pady=0)
        credit_label.grid(row=4, column=0, columnspan=5, sticky="e")

        # Center the widgets horizontally and vertically by using weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)  # Less weight means closer to the center
        self.grid_rowconfigure(2, weight=2)  # More weight pushes the 'Next' button down
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)  # Equal weights for these columns so Entry is longer
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)
            self.controller.update_selected_folder(folder_selected)

    def on_folder_path_change(self, *args):
        # Get the new folder path from the Entry widget
        folder_path = self.folder_path.get()
        # Update whatever needs to be updated when the folder path changes
        self.controller.update_selected_folder(folder_path)

    def paste_from_clipboard(self, event):
        try:
            # Get text from clipboard
            clipboard_text = self.clipboard_get()
            # Insert the clipboard text into the Entry widget at the cursor position
            event.widget.insert(tk.INSERT, clipboard_text)
        except tk.TclError:
            pass  # In case there's nothing to paste or some other error occurs

    def close_application(self):
        # This method will be called when the 'Close' button is clicked
        self.controller.quit()  # This will close the application
