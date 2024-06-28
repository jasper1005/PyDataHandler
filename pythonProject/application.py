import tkinter as tk
from folder_selection_page import FolderSelectionPage
from file_selection_page import FileSelectionPage
from SelectedFilesPage import SelectedFilesPage
from DisplaySelectedInfoPage import DisplaySelectedInfoPage
from tkinter import messagebox

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Handler")
        self.geometry("600x450")
        self.resizable(False,False)
        self.pages = {}
        self.init_pages()
        self.selected_folder = ""
        self.show_about()

    def init_pages(self):
        # Initialize and add FolderSelectionPage
        folder_selection_page = FolderSelectionPage(parent=self, controller=self)
        self.pages['FolderSelectionPage'] = folder_selection_page
        folder_selection_page.grid(row=0, column=0, sticky="nsew")

        # Initialize and add FileSelectionPage
        file_selection_page = FileSelectionPage(parent=self, controller=self)
        self.pages['FileSelectionPage'] = file_selection_page
        file_selection_page.grid(row=0, column=0, sticky="nsew")

        # Initialize and add SelectedFilesPage
        selected_files_page = SelectedFilesPage(parent=self, controller=self)
        self.pages['SelectedFilesPage'] = selected_files_page
        selected_files_page.grid(row=0, column=0, sticky="nsew")

        # Initialize and add DisplaySelectedInfoPage
        display_selected_info_page = DisplaySelectedInfoPage(parent=self, controller=self)
        self.pages['DisplaySelectedInfoPage'] = display_selected_info_page
        display_selected_info_page.grid(row=0, column=0, sticky="nsew")

        # Make sure to show the initial page
        self.show_page("FolderSelectionPage")

    def show_page(self, page_name):
        for page in self.pages.values():
            page.grid_remove()
        page = self.pages[page_name]
        page.grid()

    def update_selected_folder(self, folder_path):
        self.selected_folder = folder_path
        # Pass the file type to the FileSelectionPage
        self.pages['FileSelectionPage'].update_with_new_folder(folder_path)

    def show_selected_files_page(self, selected_files, skip_rows, sample_data):
        self.pages['SelectedFilesPage'].display_selected_files(selected_files, skip_rows, sample_data)
        self.show_page("SelectedFilesPage")

    def show_warning_message(self):
        messagebox.showwarning("Disclaimer",
                               "This software is intended for learning, teaching, or personal use purposes only.")

    def show_about(self):
        messagebox.showinfo("About",
                            "Content is copyright © Jasper Cheng (Github: jasper1005). You are permitted to use the content for personal, learning, or teaching purposes only. No trademark permissions are granted.\n\nContent based on Data Handler.")
