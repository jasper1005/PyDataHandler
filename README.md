The software is a sophisticated file selection and data management tool developed with Tkinter, designed to streamline the process of handling large datasets across various formats, including CSV, TXT, and Excel files. Users can filter files by type, preview details, and ensure structural consistency. The primary functionality includes splitting data based on unique items within a selected column or grouping specific unique items into a single file. These operations can be performed across one or multiple files, providing flexibility and efficiency for data processing tasks. The tool also offers features for selecting or deselecting all files, skipping rows, and sampling data, making it ideal for managing extensive datasets with precision.

**Instructions:**

- Select the folder containing your files by clicking 'Select Folder'.
- The selected folder path will be displayed in the text field.
- Click 'Next' to proceed to the File Selection page.

**File Selection Page:**

- Choose the type of files you want to select from the dropdown menu.
- Select the files you want to process. You can use 'Select All' or 'Deselect All' buttons.
- Specify the number of rows to skip if necessary.
- Optionally, enable 'Sample Data' to process only the first 20,000 rows.
- Click 'Next' to proceed to the Selected Files page.

**Selected Files Page:**
![image](https://github.com/jasper1005/PyDataHandler/assets/69462492/fb80a4d5-28e9-4c36-982f-2e3ca5e67826)

- Review the list of selected files and their details.
- Select a header to classify unique items from the file data.
- Click 'Next' to proceed to the Display Selected Info page.
  
**Display Selected Info Page:**

- Review the unique items and select the desired items for processing.
- Use the toggle button to switch between Split and Group modes
- Use the search bar to filter items based on conditions.
- Click 'Next' to proceed to the output options dialog.

**Output Path Selecting Page:**

- Choose the output path, file name, and format.
- Click 'Extract' to generate the output files.
