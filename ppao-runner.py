"""
#License: MIT License
Copyright (c) 2023 

You are free to:
    Share — copy and redistribute the material in any medium or format
    Adapt — remix, transform, and build upon the material

The licensor cannot revoke these freedoms as long as you follow the license terms.

Under the following terms:
    Attribution — You must give appropriate credit, provide a link to the license,
                  and indicate if changes were made. You may do so in any reasonable
                  manner, but not in any way that suggests the licensor endorses you
                  or your use.
    NonCommercial — You may not use the material for commercial purposes.
    ShareAlike — If you remix, transform, or build upon the material,
                 you must distribute your contributions under the same license
                 as the original.

More details can be found at:
https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess


class PhotoPrismUserManagementApp:

    def __init__(self, root):
        self.root = root
        self.root.title("PhotoPrism User Management")
        self.create_widgets()
        # self.list_users()

    def create_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        name = self.name_entry.get()
        role = self.role_combobox.get()

        command = f'docker compose exec photoprism photoprism users add -p "{password}" -n "{name}" -r "{role}" {username}'
        try:
            subprocess.check_output(command, shell=True, text=True)
            tk.messagebox.showinfo("Success", "User created successfully.")
        except subprocess.CalledProcessError as e:
            error_msg = f"Error: {e}\nPlease check your Docker Compose YAML file and ensure the command is correct."
            tk.messagebox.showerror("Error", error_msg)
        self.list_users()

    def list_users(self):
        command = "docker compose exec photoprism photoprism users ls"
        users = []  # Initialize the users variable as an empty list
        try:
            output = subprocess.check_output(command, shell=True, text=True)
            lines = output.split("\n")[1:-2]
            users = [line.split() for line in lines]
        except subprocess.CalledProcessError as e:
            error_msg = f"Error: {e}\nPlease check your Docker Compose YAML file and ensure the command is correct."
            tk.messagebox.showerror("Error", error_msg)

        self.users_listbox.delete(0, tk.END)
        for user in users:
            user_info = f"{user[0]} - {user[1]} - {user[2]} - {user[3]}"
            self.users_listbox.insert(tk.END, user_info)

    def create_widgets(self):
        # Create user input fields
        self.username_entry = ttk.Entry(self.root)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.root, text="Username:").grid(
            row=0, column=0, padx=5, pady=5)

        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self.root, text="Password:").grid(
            row=1, column=0, padx=5, pady=5)

        self.name_entry = ttk.Entry(self.root)
        self.name_entry.grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(self.root, text="Name:").grid(
            row=2, column=0, padx=5, pady=5)

        self.role_combobox = ttk.Combobox(self.root, values=("user", "admin"))
        self.role_combobox.grid(row=3, column=1, padx=5, pady=5)
        ttk.Label(self.root, text="Role:").grid(
            row=3, column=0, padx=5, pady=5)

        # Create user button
        self.create_user_button = ttk.Button(
            self.root, text="Create User", command=self.create_user)
        self.create_user_button.grid(
            row=4, column=0, columnspan=2, padx=5, pady=5)

        # List of users
        self.users_listbox = tk.Listbox(self.root, width=80)
        self.users_listbox.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Delete and edit buttons
        self.delete_user_button = ttk.Button(
            self.root, text="Delete User", command=self.delete_user)
        self.delete_user_button.grid(row=6, column=0, padx=5, pady=5)

        self.edit_user_button = ttk.Button(
            self.root, text="Edit User", command=self.edit_user)
        self.edit_user_button.grid(row=6, column=1, padx=5, pady=5)

        self.refresh_users_button = ttk.Button(
            self.root, text="Refresh Users", command=self.list_users)
        self.refresh_users_button.grid(
            row=7, column=0, columnspan=2, padx=5, pady=5)

    def delete_user(self):
        selected_user = self.users_listbox.get(
            self.users_listbox.curselection())
        username = selected_user.split(" - ")[0]

        command = f'docker compose exec photoprism photoprism users rm {username}'
        try:
            subprocess.check_output(command, shell=True, text=True)
            tk.messagebox.showinfo("Success", "User deleted successfully.")
            self.list_users()
        except subprocess.CalledProcessError as e:
            error_msg = f"Error: {e}\nPlease check your Docker Compose YAML file and ensure the command is correct."
            tk.messagebox.showerror("Error", error_msg)

    def edit_user(self):
        pass


root = tk.Tk()
app = PhotoPrismUserManagementApp(root)
root.mainloop()
