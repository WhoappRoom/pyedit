import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox, simpledialog
import subprocess

class PythonCodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Code Editor")
        screen_width = self.root.winfo_screenwidth()
        if screen_width < 800:
            window_width = screen_width - 20
            window_height = root.winfo_screenheight() - 100
        else:
            window_width = 800
            window_height = 600
        self.root.geometry(f"{window_width}x{window_height}")
        self.text_area = scrolledtext.ScrolledText(self.root, wrap="word")
        self.text_area.pack(expand=True, fill="both")
        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_app)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.run_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.run_menu.add_command(label="Run", command=self.run_code)
        self.run_menu.add_command(label="Install Framework", command=self.install_framework)
        self.run_menu.add_command(label="Installed Frameworks", command=self.display_installed_frameworks)
        self.run_menu.add_command(label="Update Pip", command=self.update_pip) # Add Update Pip option
        self.menu_bar.add_cascade(label="Run", menu=self.run_menu)
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.edit_menu.add_command(label="Undo", command=self.undo_text, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command=self.redo_text, accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Copy", command=self.copy_text, accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Paste", command=self.paste_text, accelerator="Ctrl+V")
        self.edit_menu.add_command(label="Select All", command=self.select_all_text, accelerator="Ctrl+A")
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.root.config(menu=self.menu_bar)
    
    def new_file(self):
        self.text_area.delete(1.0, tk.END)
    
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, content)
    
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)
    
    def exit_app(self):
        self.root.quit()
    
    def run_code(self):
        code = self.text_area.get(1.0, tk.END)
        try:
            output = subprocess.check_output(['python3', '-c', code], stderr=subprocess.STDOUT)
            output = output.decode('utf-8')
            messagebox.showinfo("Output", output)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", e.output.decode('utf-8'))
    
    def copy_text(self):
        self.text_area.clipboard_clear()
        self.select_all_text()
        selected_text = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
        self.text_area.clipboard_append(selected_text)
    
    def paste_text(self):
        text_to_paste = self.text_area.clipboard_get()
        self.text_area.insert(tk.INSERT, text_to_paste)
    
    def undo_text(self):
        self.text_area.event_generate("<<Undo>>")
    
    def redo_text(self):
        self.text_area.event_generate("<<Redo>>")
    
    def select_all_text(self):
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)
    
    def install_framework(self):
        framework = simpledialog.askstring("Install Framework", "Enter framework name:")
        if framework:
            try:
                subprocess.check_call(['pip', 'install', framework])
                messagebox.showinfo("Success", f"{framework} installed successfully!")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to install {framework}: {e}")
    
    def display_installed_frameworks(self):
        try:
            output = subprocess.check_output(['pip', 'list'], stderr=subprocess.STDOUT)
            output = output.decode('utf-8')

            # Create a new window for displaying the installed frameworks
            framework_window = tk.Toplevel(self.root)
            framework_window.title("Installed Frameworks")
            framework_window.geometry("1058x1000")

            # Create a ScrolledText widget to display the installed frameworks
            installed_frameworks_text = scrolledtext.ScrolledText(framework_window, wrap="word")
            installed_frameworks_text.pack(expand=True, fill="both")

            # Insert the installed frameworks into the ScrolledText widget
            installed_frameworks_text.insert(tk.END, output)

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", e.output.decode('utf-8'))
    
    def update_pip(self):
        try:
            subprocess.check_call(['pip', 'install', '--upgrade', 'pip'])
            messagebox.showinfo("Success", "Pip has been updated successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to update pip: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PythonCodeEditor(root)
    root.mainloop()
