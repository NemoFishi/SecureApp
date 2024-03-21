import hashlib
import tkinter as tk
from tkinter import messagebox
from secureChecker import *
from mySQLDatabase import conn


class LoginPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.login_button = None
        self.password_entry = None
        self.username_entry = None
        self.grid()
        self.create_widgets()
        register_button = tk.Button(self, text="Register", command=lambda: master.switch_frame("RegistrationPage"))
        register_button.grid(row=3, column=0, padx=(10, 10))

    def create_widgets(self):
        # Title Label
        tk.Label(self, text="Login Page").grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # Username Label and Entry
        tk.Label(self, text="Username").grid(row=1, column=0, padx=(10, 10), sticky=tk.W)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=1, column=1, padx=(10, 10), pady=(0, 10), sticky=tk.EW)
        self.username_entry.bind("<Return>", lambda event: self.login())

        # Password Label and Entry
        tk.Label(self, text="Password").grid(row=2, column=0, padx=(10, 10), sticky=tk.W)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1, padx=(10, 10), pady=(0, 10), sticky=tk.EW)
        self.password_entry.bind("<Return>", lambda event: self.login())

        # Login Button
        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.grid(row=3, column=0, columnspan=2)

        # Configure the grid to expand the entry fields with the window
        self.grid_columnconfigure(1, weight=1)

    def login(self):
        newUsername = sanitize(self.username_entry.get())
        newPassword = sanitize(self.password_entry.get())

        myConn = conn.cursor()
        # Parameterized Query to check for newUsername
        myConn.execute("SELECT * FROM userdata WHERE Username = %s", (newUsername,))

        # Fetch the results
        check = myConn.fetchone()

        if check is not None:
            # Assuming the password and salt are stored in columns 3 and 4
            hashed_password = check[3]
            salt = check[4]

            # Concatenate the provided password with the retrieved salt
            salted_password = newPassword + salt

            # Hash the salted password using SHA-256
            hashed_input_password = hashlib.sha256(salted_password.encode()).hexdigest()

            # Compare the hashed input password with the stored hashed password
            if hashed_input_password == hashed_password:
                print("Login successful!")
                messagebox.showinfo(title="Login Success", message="Login Successful")
                self.master.switch_frame("WebScraper")
            else:
                print("Incorrect password. Please try again.")
                messagebox.showinfo(title="Login Fail", message="Incorrect password.")
        else:
            print("Username not found.")
            messagebox.showinfo(title="Login Fail", message="Username not found")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginPage(root)
    app.pack()
    root.mainloop()
