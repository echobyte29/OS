import tkinter as tk
from tkinter import messagebox, filedialog
import os

# Function to create a new file
def create_file():
    file_name = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", ".txt"), ("All files", ".*")])
    if file_name:
        try:
            with open(file_name, 'w') as f:
                f.write("")
            update_file_list()
            messagebox.showinfo("Success", f"File '{os.path.basename(file_name)}' created.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create file: {e}")

# Function to edit a file
def edit_file():
    selected_file = file_listbox.get(tk.ACTIVE)
    if selected_file:
        try:
            with open(selected_file, 'r') as f:
                content = f.read()

            # Open a new window for editing
            edit_window = tk.Toplevel(root)
            edit_window.title(f"Edit {selected_file}")
            edit_window.geometry("600x400")

            # Frame for Save button and text area
            frame = tk.Frame(edit_window)
            frame.pack(fill=tk.BOTH, expand=True)

            # Function to save the edited content back to the file
            def save_edit():
                with open(selected_file, 'w') as f:
                    f.write(text_area.get(1.0, tk.END).strip())
                messagebox.showinfo("Success", f"File '{selected_file}' edited.")
                edit_window.destroy()

            # Save button at the top
            save_button = tk.Button(frame, text="Save", command=save_edit, bg="#5cb85c", fg="white", font=("Arial", 10, "bold"))
            save_button.pack(side=tk.TOP, pady=10)

            # Text area to edit the file content
            text_area = tk.Text(frame, wrap=tk.WORD, font=("Arial", 12), bg="#f4f4f4", fg="#333")
            text_area.insert(1.0, content)
            text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to edit file: {e}")

# Function to delete a file
def delete_file():
    selected_file = file_listbox.get(tk.ACTIVE)
    if selected_file:
        confirmation = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{selected_file}'?")
        if confirmation:
            try:
                os.remove(selected_file)
                update_file_list()  # Update the file list after deletion
                messagebox.showinfo("Success", f"File '{selected_file}' deleted.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete file: {e}")

# Function to rename a file
def rename_file():
    selected_file = file_listbox.get(tk.ACTIVE)
    if selected_file:
        new_name = filedialog.asksaveasfilename(initialfile=selected_file, defaultextension=".txt", filetypes=[("All files", ".")])
        if new_name:
            try:
                os.rename(selected_file, new_name)
                update_file_list()  # Update the file list after renaming
                messagebox.showinfo("Success", f"File renamed to '{new_name}'.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rename file: {e}")

# Function to update the list of files in the current directory
def update_file_list():
    file_listbox.delete(0, tk.END)
    files = [f for f in os.listdir(".") if os.path.isfile(f) and not f.startswith('.')]
    for file_name in sorted(files):
        file_listbox.insert(tk.END, file_name)

    # Disable buttons if there are no files in the directory
    if not files:
        edit_button.config(state=tk.DISABLED)
        delete_button.config(state=tk.DISABLED)
        rename_button.config(state=tk.DISABLED)

# Function to enable buttons when a file is selected
def on_file_select(event):
    selected_file = file_listbox.curselection()
    if selected_file:
        edit_button.config(state=tk.NORMAL)
        delete_button.config(state=tk.NORMAL)
        rename_button.config(state=tk.NORMAL)
    else:
        edit_button.config(state=tk.DISABLED)
        delete_button.config(state=tk.DISABLED)
        rename_button.config(state=tk.DISABLED)

# Main Window Setup
root = tk.Tk()
root.title("File Explorer System")
root.geometry("700x500")
root.configure(bg="#222")

# Title Label (Updated)
title_label = tk.Label(root, text="FileWizz 📝", font=("Helvetica", 28, "bold"), bg="#222", fg="white")
title_label.pack(pady=20)

# Frame for the file list and buttons
main_frame = tk.Frame(root, bg="#222")
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# File Listbox
file_listbox = tk.Listbox(main_frame, height=20, width=50, font=("Arial", 12), bg="#333", fg="white", selectbackground="#5cb85c", selectforeground="white")
file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar
scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=file_listbox.yview)
file_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)

# Button Frame
button_frame = tk.Frame(main_frame, bg="#222")
button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20)

# Create button
create_button = tk.Button(button_frame, text="Create", command=create_file, bg="#5cb85c", fg="white", font=("Arial", 12, "bold"), width=15)
create_button.pack(pady=10)

# Edit button
edit_button = tk.Button(button_frame, text="Edit", command=edit_file, bg="#0275d8", fg="white", font=("Arial", 12, "bold"), width=15, state=tk.DISABLED)
edit_button.pack(pady=10)

# Delete button
delete_button = tk.Button(button_frame, text="Delete", command=delete_file, bg="#d9534f", fg="white", font=("Arial", 12, "bold"), width=15, state=tk.DISABLED)
delete_button.pack(pady=10)

# Rename button
rename_button = tk.Button(button_frame, text="Rename", command=rename_file, bg="#f0ad4e", fg="white", font=("Arial", 12, "bold"), width=15, state=tk.DISABLED)
rename_button.pack(pady=10)

# Bind file selection to enable buttons
file_listbox.bind('<<ListboxSelect>>', on_file_select)

# Populate the listbox with files when the app starts
update_file_list()

# Developed by Label at the Bottom
footer_label = tk.Label(root, text="developed with ❤️by Team Rasmalai", font=("Helvetica", 12), bg="#222", fg="white")
footer_label.pack(side=tk.BOTTOM, pady=10)

# Run the application
root.mainloop()
