import tkinter as tk
from tkinter import simpledialog
import requests
from bs4 import BeautifulSoup
# some code from https://www.zenrows.com/blog/web-scraping-login-python#waf-protected-websites
# thank you for the assistance website!

class WebScraper(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Adjust the window size when the PageTwo screen is loaded
        master.geometry('500x520')

        # URL Entry
        self.url_label = tk.Label(self, text="Enter GitHub Username:")
        self.url_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        self.username_entry = tk.Entry(self, width=30)
        self.username_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")
        self.username_entry.bind("<Return>", lambda event: self.scrape_github())

        # Button to trigger the GitHub scraping
        self.scrape_button = tk.Button(self, text="Scrape GitHub", command=self.scrape_github)
        self.scrape_button.grid(row=1, column=0, columnspan=1)

        # Create a Text widget to display the scraped content
        self.text_area = tk.Text(self, height=10, width=50)
        self.text_area.grid(row=2, column=0, columnspan=2, pady=20, padx=10, sticky="nsew")

    def get_password(self):
        # Prompt user for GitHub password
        password = simpledialog.askstring("Password", "Enter GitHub Password:", show='*')
        return password

    def scrape_github(self):
        # Get the GitHub username from the entry
        username = self.username_entry.get()

        # Get the GitHub password
        password = self.get_password()

        if not password:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, "No password entered.")
            return

        # Construct URLs
        login_url = "https://github.com/session"
        repos_url = "https://github.com/" + username + "/?tab=repositories"

        with requests.session() as s:
            req = s.get(login_url).text
            html = BeautifulSoup(req, "html.parser")
            token = html.find("input", {"name": "authenticity_token"}).attrs["value"]
            time = html.find("input", {"name": "timestamp"}).attrs["value"]
            timeSecret = html.find("input", {"name": "timestamp_secret"}).attrs["value"]

            payload = {
                "authenticity_token": token,
                "login": username,
                "password": password,
                "timestamp": time,
                "timestamp_secret": timeSecret
            }
            res = s.post(login_url, data=payload)

            r = s.get(repos_url)
            soup = BeautifulSoup(r.content, "html.parser")
            usernameDiv = soup.find("span", class_="p-nickname vcard-username d-block")

            # Clear the Text widget
            self.text_area.delete(1.0, tk.END)

            # Display the scraped content in the Text widget
            self.text_area.insert(tk.END, "GitHub Username: " + usernameDiv.getText() + "\n")

            repos = soup.find_all("h3", class_="wb-break-all")
            for r in repos:
                repoName = r.find("a").getText()
                self.text_area.insert(tk.END, "Repository Name: " + repoName + "\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = WebScraper(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
