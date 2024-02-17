import tkinter as tk
from urllib.parse import urlparse
from linkwiz.browser import get_installed_browsers
from linkwiz.open import open_link
from linkwiz.config import custom_browsers, custom_rules

class LinkwizApp:
    def __init__(self, browsers, url):
        self.url = url
        self.browsers = browsers
        self.root = tk.Tk()
        self.root.title("LinkWiz")
        self.root.resizable(False, False)

        self.buttons = []
        self._create_button()

        self.root.bind("<Key>", self.on_key_pressed)

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
        if event.char.isdigit():
            index = int(event.char) - 1
            if 0 <= index < len(self.browsers):
                self.open_selected_browser(index)

    def open_selected_browser(self, index):
        """Opens the selected browser with the given URL."""
        selected_browser = list(self.browsers.values())[index]
        try:
            open_link(selected_browser, self.url)
            self.root.destroy()
        except Exception as e:
            print(f"Error opening link: {e}")

    def run(self):
        self.root.mainloop()
