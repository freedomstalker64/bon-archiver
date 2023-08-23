import tkinter as tk
from tkinter import filedialog, ttk
import lzma
import pickle
import os

class BonArchiverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bon Archiver")

        self.compress_button = tk.Button(self.root, text="Compress", command=self.compress)
        self.compress_button.pack()

        self.extract_button = tk.Button(self.root, text="Extract", command=self.extract)
        self.extract_button.pack()

        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack()

    def compress(self):
        paths = filedialog.askopenfilenames(title="Select files or folders to compress", filetypes=[("All Files", "*.*")])
        if not paths:
            return

        output_filename = filedialog.asksaveasfilename(defaultextension=".bon", filetypes=[("Bon Files", "*.bon")])
        if not output_filename:
            return

        files_data = []

        total_files = len(paths)
        self.progress_bar["maximum"] = total_files
        self.progress_bar["value"] = 0

        for i, path in enumerate(paths, start=1):
            self.progress_bar["value"] = i
            self.root.update()

            if os.path.isfile(path):
                with open(path, 'rb') as f_in:
                    data = f_in.read()
                    files_data.append((path, data))
            elif os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        with open(file_path, 'rb') as f_in:
                            data = f_in.read()
                            files_data.append((file_path, data))

        with lzma.open(output_filename, 'wb', preset=lzma.PRESET_EXTREME) as f_out:
            pickle.dump(files_data, f_out)

        print("Compression complete!")

    def extract(self):
        compressed_path = filedialog.askopenfilename(title="Select compressed file to extract", filetypes=[("Bon Files", "*.bon")])
        if not compressed_path:
            return

        output_folder = filedialog.askdirectory(title="Select extraction folder")
        if not output_folder:
            return

        with lzma.open(compressed_path, 'rb') as f_in:
            files_data = pickle.load(f_in)

            total_files = len(files_data)
            self.progress_bar["maximum"] = total_files
            self.progress_bar["value"] = 0

            for i, (file_path, data) in enumerate(files_data, start=1):
                self.progress_bar["value"] = i
                self.root.update()

                file_name = os.path.basename(file_path)
                file_full_path = os.path.join(output_folder, file_name)

                with open(file_full_path, 'wb') as f_out:
                    f_out.write(data)

        print("Extraction complete!")

def main():
    root = tk.Tk()
    app = BonArchiverApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
