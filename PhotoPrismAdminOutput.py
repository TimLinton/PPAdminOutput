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


class PhotoPrismUserManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PhotoPrism User Management")
        self.create_widgets()

    def list_legacy_users(self):
        command = "docker compose exec photoprism photoprism users legacy"
        self.update_command_output(command)

    def show_user(self):

        command = f'docker compose exec photoprism photoprism users show username'
        self.update_command_output(command)

    def reset_users(self):
        command = "docker compose exec photoprism photoprism users reset"
        self.update_command_output(command)

    def create_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        name = self.name_entry.get()
        role = self.role_combobox.get()
        email = self.email_entry.get()
        superadmin = self.superadmin_var.get()
        no_login = self.no_login_var.get()
        webdav = self.webdav_var.get()
        upload_path = self.upload_path_entry.get()

        command = f'docker compose exec photoprism photoprism users add -p "{password}" -n "{name}" -r "{role}"'
        if email:
            command += f' -m "{email}"'
        if superadmin:
            command += ' -s'
        if no_login:
            command += ' -l'
        if webdav:
            command += ' -w'
        if upload_path:
            command += f' -u "{upload_path}"'
        command += f' {username}'

        self.update_command_output(command)

    def list_users(self):
        command = "docker compose exec photoprism photoprism users ls"
        self.update_command_output(command)
        # out put the command 'command' to the text box so the user can copy the command and run it in the terminal

    def update_command_output(self, command):
        self.command_output.delete(1.0, tk.END)
        if command.strip():  # Check if the command is not empty or only contains whitespaces
            self.command_output.insert(tk.END, command)

    def create_widgets(self):
        # User Information
        user_frame = ttk.LabelFrame(self.root, text="User Information")
        user_frame.grid(row=0, column=0, padx=3, pady=3, sticky="w")

        ttk.Label(user_frame, text="Username:").grid(
            row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(user_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(user_frame, text="Password:").grid(
            row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(user_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(user_frame, text="Name:").grid(
            row=2, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(user_frame)
        self.name_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(user_frame, text="Email:").grid(
            row=3, column=0, padx=5, pady=5)
        self.email_entry = ttk.Entry(user_frame)
        self.email_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(user_frame, text="Role:").grid(
            row=4, column=0, padx=5, pady=5)
        self.role_combobox = ttk.Combobox(user_frame, values=(
            "admin", "user", "viewer", "guest", "visitor"))
        self.role_combobox.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(user_frame, text="Upload Path:").grid(
            row=5, column=0, padx=5, pady=5)
        self.upload_path_entry = ttk.Entry(user_frame)
        self.upload_path_entry.grid(row=5, column=1, padx=5, pady=5)

        # User Permissions
        perm_frame = ttk.LabelFrame(self.root, text="User Permissions")
        perm_frame.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.superadmin_var = tk.BooleanVar()
        self.superadmin_checkbox = ttk.Checkbutton(
            perm_frame, text="Super Admin", variable=self.superadmin_var)
        self.superadmin_checkbox.grid(row=0, column=0, padx=5, pady=5)

        self.no_login_var = tk.BooleanVar()
        self.no_login_checkbox = ttk.Checkbutton(
            perm_frame, text="No Login", variable=self.no_login_var)
        self.no_login_checkbox.grid(row=0, column=1, padx=5, pady=5)

        self.webdav_var = tk.BooleanVar()
        self.webdav_checkbox = ttk.Checkbutton(
            perm_frame, text="WebDAV", variable=self.webdav_var)
        self.webdav_checkbox.grid(row=1, column=0, padx=5, pady=5)

        self.tokens_var = tk.BooleanVar()
        self.tokens_checkbox = ttk.Checkbutton(
            perm_frame, text="Tokens", variable=self.tokens_var)
        self.tokens_checkbox.grid(row=1, column=1, padx=5, pady=5)

        # User Actions
        action_frame = ttk.LabelFrame(self.root, text="User Actions")
        action_frame.grid(row=1, column=0, columnspan=2,
                          padx=5, pady=5, sticky="w")

        self.create_user_button = ttk.Button(
            action_frame, text="Create User", command=self.create_user)
        self.create_user_button.grid(row=0, column=0, padx=5, pady=5)

        self.delete_user_button = ttk.Button(
            action_frame, text="Delete User", command=self.delete_user)
        self.delete_user_button.grid(row=0, column=1, padx=5, pady=5)

        self.edit_user_button = ttk.Button(
            action_frame, text="Edit User", command=self.edit_user)
        self.edit_user_button.grid(row=0, column=2, padx=5, pady=5)

        # User List
        list_frame = ttk.LabelFrame(self.root, text="User List")
        list_frame.grid(row=2, column=0, columnspan=2,
                        padx=5, pady=5, sticky="w")

        self.md_var = tk.BooleanVar()
        self.md_checkbox = ttk.Checkbutton(
            list_frame, text="Markdown", variable=self.md_var)
        self.md_checkbox.grid(row=0, column=0, padx=5, pady=5)

        self.csv_var = tk.BooleanVar()
        self.csv_checkbox = ttk.Checkbutton(
            list_frame, text="CSV", variable=self.csv_var)
        self.csv_checkbox.grid(row=0, column=1, padx=5, pady=5)

        self.tsv_var = tk.BooleanVar()
        self.tsv_checkbox = ttk.Checkbutton(
            list_frame, text="TSV", variable=self.tsv_var)
        self.tsv_checkbox.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(list_frame, text="Limit:").grid(
            row=1, column=0, padx=5, pady=5)
        self.limit_entry = ttk.Entry(list_frame)
        self.limit_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(list_frame, text="Search:").grid(
            row=1, column=2, padx=5, pady=5)
        self.search_entry = ttk.Entry(list_frame)

        self.list_users_button = ttk.Button(
            list_frame, text="List Users", command=self.list_users)
        self.list_users_button.grid(row=1, column=3, padx=5, pady=5)

        # Command Output

        output_frame = ttk.LabelFrame(self.root, text="Command Output")
        output_frame.grid(row=3, column=0, columnspan=2,
                          padx=3, pady=3, sticky="w")

        self.command_output = tk.Text(output_frame, height=8, width=80)
        self.command_output.grid(row=0, column=0, padx=3, pady=3)

    def delete_user(self):

        command = f'docker compose exec photoprism photoprism users rm username'
        self.update_command_output(command)

    def list_users(self):
        search_term = self.search_entry.get()
        md = self.md_var.get()
        csv = self.csv_var.get()
        tsv = self.tsv_var.get()
        limit = self.limit_entry.get()
        tokens = self.tokens_var.get()

        command = 'photoprism users ls'
        if md:
            command += ' --md'
        if csv:
            command += ' --csv'
        if tsv:
            command += ' --tsv'
        if limit:
            command += f' -n {limit}'
        if tokens:
            command += ' --tokens'
        if search_term:
            command += f' "{search_term}"'

        self.update_command_output(command)

    def edit_user(self):
        username = self.username_entry.get()
        if username:
            password = self.password_entry.get()
            name = self.name_entry.get()
            role = self.role_combobox.get()
            email = self.email_entry.get()
            superadmin = self.superadmin_var.get()
            no_login = self.no_login_var.get()
            webdav = self.webdav_var.get()
            upload_path = self.upload_path_entry.get()

            command = f'photoprism users mod'
            if password:
                command += f' -p "{password}"'
            if name:
                command += f' -n "{name}"'
            if role:
                command += f' -r "{role}"'
            if email:
                command += f' -m "{email}"'
            if superadmin:
                command += ' -s'
            if no_login:
                command += ' -l'
            if webdav:
                command += ' -w'
            if upload_path:
                command += f' -u "{upload_path}"'
            command += f' {username}'

            self.update_command_output(command)
        else:
            self.command_output.delete(1.0, tk.END)
            self.command_output.insert(tk.END, "Please enter a username.")


root = tk.Tk()
app = PhotoPrismUserManagementApp(root)
root.mainloop()
