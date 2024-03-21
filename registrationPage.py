import tkinter as tk
from tkinter import messagebox
from secureChecker import *


class RegistrationPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Registration Page").grid(row=0, column=0, columnspan=2, pady=10)

        # Labels for inputs
        tk.Label(self, text="Input Name:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Label(self, text="Input Username:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        tk.Label(self, text="Input Password:").grid(row=3, column=0, padx=10, pady=5, sticky="e")

        # Entries for inputs
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.name_entry.bind("<Return>", lambda event: self.finalize_account())
        self.name_entry.bind("<Escape>", lambda event: self.master.switch_frame("LoginPage"))

        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.username_entry.bind("<Return>", lambda event: self.finalize_account())
        self.username_entry.bind("<Escape>", lambda event: self.master.switch_frame("LoginPage"))

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.password_entry.bind("<Return>", lambda event: self.finalize_account())
        self.password_entry.bind("<Escape>", lambda event: self.master.switch_frame("LoginPage"))

        # Labels for requirements
        tk.Label(self, text="Name must be 3-15 characters long and can only contain letters",
                 wraplength=400).grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        tk.Label(self, text="Username must be 4-20 characters long and can only contain letters, numbers, "
                            "and underscores.", wraplength=400).grid(row=5, column=0, columnspan=2, padx=10, pady=5,
                                                                     sticky="w")
        tk.Label(self, text="Password must be 8-20 characters long and contain at least one lowercase letter, "
                            "one uppercase letter, and one digit.", wraplength=400).grid(row=6, column=0,
                                                                                         columnspan=2, padx=10, pady=5,
                                                                                         sticky="w")

        # Buttons
        createAccount_btn = tk.Button(self, text="Create Account", command=self.finalize_account)
        createAccount_btn.grid(row=7, column=1, pady=20)

        alreadyUser_btn = tk.Button(self, text="Already User? Log in!",
                                    command=lambda: self.master.switch_frame("LoginPage"))
        alreadyUser_btn.grid(row=7, column=0, padx=20, sticky="w")

    def finalize_account(self):
        try:
            # Get user inputs
            name = sanitize(self.name_entry.get())
            newUsername = sanitize(self.username_entry.get())
            newPassword = sanitize(self.password_entry.get())

            if 'SELECT' in self.name_entry.get() or 'SELECT' in self.username_entry.get() or 'SELECT' in self.password_entry.get():
                raise ValueError("Input contained harmful keywords!")
            elif 'DROP' in self.name_entry.get() or 'DROP' in self.username_entry.get() or 'DROP' in self.password_entry.get():
                raise ValueError("Input contained harmful keywords!")
            elif 'DELETE' in self.name_entry.get() or 'DELETE' in self.username_entry.get() or 'DELETE' in self.password_entry.get():
                raise ValueError("Input contained harmful keywords!")

            # Validate username and password
            if not validate_name(name):
                raise ValueError("Invalid Name!")
            if not validate_username(newUsername):
                raise ValueError("Invalid Username!")
            if not validate_password(newPassword):
                raise ValueError("Invalid Password!")

            # Check if the username already exists
            if username_exists(newUsername):
                raise ValueError("Username already exists!")

            # Call the createUser stored procedure with parameters
            objectCurser = conn.cursor()
            objectCurser.callproc('createUser', (name, newUsername, newPassword))
            conn.commit()

            messagebox.showinfo("Success", "Account created successfully!")
            self.master.switch_frame("LoginPage")

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    # noinspection PyArgumentList
    root = RegistrationPage()
    root.mainloop()
