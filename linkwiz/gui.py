import tkinter as tk
from urllib.parse import urlparse
from linkwiz.config import config
from typing import Dict
from tkinter import ttk
import logging


class LinkwizGUI:

    def __init__(self, browsers: Dict[str, str], url: str):
        self.url = url
        self.hostname = urlparse(url).netloc
        self.browsers = browsers

        self.root = tk.Tk()
        self.root.title("LinkWiz")
        self.root.resizable(False, False)

        self.buttons = []
        self._create_widgets()
        self._bind_key_events()
        self._center_window()

    def _center_window(self):
        """Center the window on the screen."""
        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = max(0, (screen_width - window_width) // 2)
        y = max(0, (screen_height - window_height) // 2)
        self.root.geometry(f"+{x}+{y}")

    def _create_widgets(self):
        """Create widgets."""
        self._create_buttons()
        self._create_remember_check()

    def _create_buttons(self):
        """Create buttons for each browser."""
        for i, (browser_name, _) in enumerate(self.browsers.items()):
            button_text = f"{i+1}. {browser_name}"
            button = tk.Button(
                self.root,
                text=button_text,
                command=lambda idx=i: self.get_launch_cmd(idx),
            )
            button.pack(fill=tk.X)
            self.buttons.append(button)

    def _create_remember_check(self):
        """Create 'Remember' checkbox."""
        self.remember = tk.BooleanVar()
        self.remember_check = ttk.Checkbutton(
            self.root, text="Remember", variable=self.remember
        )
        self.remember_check.pack()

    def _bind_key_events(self):
        """Bind key press events."""
        try:
            self.root.bind("<Key>", self.on_key_pressed)
        except Exception as e:
            logging.error(f"Error binding key press: {e}")

    def on_key_pressed(self, event: tk.Event) -> None:
        """Handle key press events."""
        try:
            if event.char.isdigit():
                index = int(event.char) - 1
                if 0 <= index < len(self.browsers):
                    self.get_launch_cmd(index)
            elif event.char.lower() == "r":
                self.remember.set(not self.remember.get())
            elif event.char.lower() == "q" or event.char == "\x1b":
                self.root.destroy()
        except Exception as e:
            logging.error(f"Error handling key press: {e}")

    def get_launch_cmd(self, index):
        """Opens the selected browser with the given URL."""
        try:
            selected_browser_name = list(self.browsers.keys())[index]
            selected_browser = self.browsers[selected_browser_name]
            if self.remember.get():
                config.add_rules(self.hostname, selected_browser_name)
            # launch_browser(selected_browser, self.url)
            self.result = selected_browser, self.url
            self.root.destroy()
        except Exception as e:
            logging.error(f"Error opening browser: {e}")

    def run(self):
        """Run the application."""
        self.root.mainloop()
        return self.result
