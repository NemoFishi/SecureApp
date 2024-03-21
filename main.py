import tkinter as tk

from loginPage import LoginPage
from registrationPage import RegistrationPage
from webScraper import WebScraper

pages = {
    "LoginPage": LoginPage,
    "RegistrationPage": RegistrationPage,
    "WebScraper": WebScraper
}


class WebScraperApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('500x520')
        self.title("Main Form")
        self._frame = None
        self.switch_frame("LoginPage")

    def switch_frame(self, page_name):
        # Destroys current frame and replaces it with a new one.
        cls = pages[page_name]
        new_frame = cls(master=self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    root = WebScraperApp()
    root.mainloop()
