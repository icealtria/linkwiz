import tkinter as tk
from urllib.parse import urlparse
from linkwiz.config import config
from linkwiz.launch import launch_browser
from typing import Dict
from tkinter import ttk
import logging

class LinkwizApp:

    def __init__(self, browsers: Dict[str, str], url: str):
        self.url = url
        self.hostname = urlparse(url).hostname
        self.browsers = browsers
        self.root = tk.Tk()
        self.root.title("LinkWiz")
        self.root.resizable(False, False)

        self.buttons = []
        self._create_button()

        self.remember = tk.BooleanVar()
        self.remember_check = ttk.Checkbutton(
            self.root, text="Remember", variable=self.remember
        )
        self.remember_check.pack()

        try:
            self.root.bind("<Key>", self.on_key_pressed)
        except Exception as e:
            logging.error(f"Error binding key press: {e}")

    def _create_button(self):
        for i, (browser_name, _) in enumerate(self.browsers.items()):
            button_text = f"{i+1}. {browser_name}"
            button = tk.Button(
                self.root,
                text=button_text,
                command=lambda idx=i: self.open_selected_browser(idx),
            )
            button.pack(fill=tk.X)
            self.buttons.append(button)

    def on_key_pressed(self, event):
        try:
            if event.char.isdigit():
                index = int(event.char) - 1
                if 0 <= index < len(self.browsers):
                    self.open_selected_browser(index)
            elif event.char.lower() == 'r':
                self.remember.set(not self.remember.get())
        except Exception as e:
            logging.error(f"Error handling key press: {e}")

    def open_selected_browser(self, index):
        """Opens the selected browser with the given URL."""
        try:
            selected_browser_name = list(self.browsers.keys())[index]
            selected_browser = self.browsers[selected_browser_name]
            if self.remember.get():
                config.add_rules(self.hostname, selected_browser_name)
            launch_browser(selected_browser, self.url)
        except Exception as e:
            logging.error(f"Error opening browser: {e}")

    def run(self):
        self.root.mainloop()
