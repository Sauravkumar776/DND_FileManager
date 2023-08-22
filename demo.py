import tkinter as tk
from tkinter import filedialog, messagebox, Scrollbar, Frame
import shelve
import os
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD

class Uploader:
    def __init__(self, root):
        self.root = root
        self.root.title("File Uploader")
        self.file_list = []

        self.db = shelve.open('file_list')

        if 'files' in self.db:
            self.file_list = self.db['files']

        self.create_widgets()

    def create_widgets(self):
        # Create a frame for file content display
        self.text_frame = Frame(self.root)
        self.text_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.selected_file_label = tk.Label(self.text_frame, text="Selected File:")
        self.selected_file_label.pack(anchor="w")

        self.text_widget = tk.Text(self.text_frame, wrap=tk.WORD, width=70, height=20)  # Adjust width and height as needed
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.text_scrollbar = Scrollbar(self.text_frame, command=self.text_widget.yview)
        self.text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.config(yscrollcommand=self.text_scrollbar.set)


        # Bind drop events to the root window
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)

        # Create a frame for buttons at the bottom
        self.button_frame = Frame(self.root)
        self.button_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

        browse_button = tk.Button(self.button_frame, text="Browse Files", command=self.browse_files)
        browse_button.pack(side=tk.LEFT, padx=5, pady=5)

        upload_button = tk.Button(self.button_frame, text="Upload Files", command=self.upload_files)
        upload_button.pack(side=tk.LEFT, padx=5, pady=5)

        delete_button = tk.Button(self.button_frame, text="Delete Selected", command=self.delete_selected_file)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create a Treeview for uploaded files
        self.file_tree = ttk.Treeview(self.root, columns=("File Name", "Size"), show="headings")
        self.file_tree.heading("File Name", text="File Name")
        self.file_tree.heading("Size", text="Size")
        self.file_tree.column("File Name", width=300, anchor="w")
        self.file_tree.column("Size", width=100, anchor="center")
        self.file_tree.pack(fill=tk.BOTH, expand=True)

        # Bind drop event to the file_tree widget
        self.file_tree.drop_target_register(DND_FILES)
        self.file_tree.dnd_bind('<<Drop>>', self.on_drop)

        for file_name in self.file_list:
            file_size = self.get_file_size(file_name)
            self.file_tree.insert("", "end", values=(file_name, file_size))

        # Bind the Treeview selection event to display selected file's content
        self.file_tree.bind("<ButtonRelease-1>", self.display_selected_file_content)

        self.progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=200, mode='determinate')
        self.progress_bar.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def browse_files(self):
        file_name = filedialog.askopenfilename()

        if file_name:
            self.file_list.append(file_name)
            file_size = self.get_file_size(file_name)
            self.file_tree.insert("", "end", values=(file_name, file_size))

            self.db['files'] = self.file_list

    def delete_selected_file(self):
        selected_item = self.file_tree.selection()
        if selected_item:
            selected_file = self.file_tree.item(selected_item)['values'][0]
            self.file_list.remove(selected_file)
            self.file_tree.delete(selected_item)

            self.db['files'] = self.file_list
            self.text_widget.delete(1.0, tk.END)  # Clear the content area when a file is deleted

    def on_drop(self, event):
        files = event.data

        if isinstance(files, str):
            # Remove curly braces from the file path
            file_path = files.strip('{}')
            files = [file_path]

        print("Dropped files:")
        for file_path in files:
            print(file_path)

        for file_path in files:
            if os.path.isfile(file_path):
                self.add_file(file_path)

        self.update_file_tree()

    def add_file(self, file_path):
        self.file_list.append(file_path)

    def update_file_tree(self):
        self.file_tree.delete(*self.file_tree.get_children())
        for file_name in self.file_list:
            file_size = self.get_file_size(file_name)
            self.file_tree.insert("", "end", values=(file_name, file_size))
        self.db['files'] = self.file_list
    def upload_files(self):
        if not self.file_list:
            messagebox.showerror("Error", "No files selected!")
            return

        self.progress_bar['value'] = 0

        for i, file_name in enumerate(self.file_list):
            self.progress_bar['value'] = (i + 1) * 100 / len(self.file_list)
            self.root.update_idletasks()

            # Simulate the file upload process (replace with your actual upload code)
            uploaded_content = self.simulate_file_upload(file_name)
            self.display_uploaded_content(uploaded_content)

        self.file_list = []
        self.file_tree.delete(*self.file_tree.get_children())
        self.db['files'] = self.file_list

        messagebox.showinfo("Success", "Files uploaded successfully!")

    def simulate_file_upload(self, file_name):
        print(f"Uploading file {file_name}...")  # Replace with actual upload logic
        # Your upload code here
        # For example: upload_file_to_server(file_name)
        # Simulate uploaded content
        return f"Content of {file_name}"

    def display_selected_file_content(self, event):
        selected_item = self.file_tree.selection()
        if selected_item:
            selected_file = self.file_tree.item(selected_item)['values'][0]
            try:
                with open(selected_file, 'r') as file:
                    content = file.read()
                    self.text_widget.delete(1.0, tk.END)
                    self.text_widget.insert(tk.END, content)
                    self.selected_file_label.config(text=f"Selected File: {selected_file}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file content: {str(e)}")

    @staticmethod
    def get_file_size(file_path):
        try:
            return f"{round(os.path.getsize(file_path) / 1024, 2)} KB"
        except Exception as e:
            return "N/A"

    def __del__(self):
        self.db.close()

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = Uploader(root)
    root.mainloop()