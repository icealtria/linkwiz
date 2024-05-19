import tkinter as tk
from urllib.parse import urlparse
from linkwiz.config import config
from typing import Dict
import logging


class ToolTip:
    """Class to manage tooltips for Tkinter widgets."""

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        """Display the tooltip."""
        if self.tip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw,
            text=self.text,
            justify="left",
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("tahoma", "8", "normal"),
        )
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        """Hide the tooltip."""
        if self.tip_window:
            self.tip_window.destroy()
        self.tip_window = None


class LinkwizGUI:
    def __init__(self, browsers: Dict[str, str], url: str):
        self.url = url
        self.hostname = urlparse(url).netloc
        self.browsers = browsers

        self.root = tk.Tk()
        self.root.title("LinkWiz")
        self.root.resizable(False, False)
        self.root.wm_minsize(width=200, height=0)
        self.root.configure(bg="white")

        self.frame = tk.Frame(self.root, bg="white")
        self.frame.pack(pady=5)

        self.buttons = []
        self._create_widgets()
        self._bind_key_events()
        self._center_window()

    def _center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = max(0, (screen_width - window_width) // 2)
        y = max(0, (screen_height - window_height) // 2)
        self.root.geometry(f"+{x}+{y}")

    def _create_widgets(self):
        """Create widgets."""
        self._create_url_label()
        self._create_buttons()
        self._create_remember_check()

    def _create_url_label(self):
        """Create a label to display the URL."""
        display_url = self._get_display_url()
        self.url_label = tk.Label(
            self.root,
            text=display_url,
            bg="white",
            fg="black",
        )
        self.url_label.pack(anchor=tk.W, padx=10)
        ToolTip(self.url_label, self.url)

    def _get_display_url(self):
        """Get the URL with the path replaced by '~'."""
        parsed_url = urlparse(self.url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}/~"

    def _create_buttons(self):
        """Create buttons for each browser."""
        for i, (browser_name, _) in enumerate(self.browsers.items()):
            button_text = f"{i+1}. {browser_name}"
            button = CustomButton(
                self.frame,
                text=button_text,
                command=lambda idx=i: self.get_launch_cmd(idx),
                anchor="w",
            )
            button.pack(fill=tk.X, padx=10, pady=5)
            self.buttons.append(button)

    def _create_remember_check(self):
        """Create 'Remember' checkbox."""
        self.remember = tk.BooleanVar()
        self.remember_check = CustomCheckbutton(
            self.root, text="Remember", variable=self.remember
        )
        self.remember_check.pack(anchor=tk.W, padx=10)

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
        selected_browser_name = list(self.browsers.keys())[index]
        selected_browser = self.browsers[selected_browser_name]
        if self.remember.get():
            config.add_rules(self.hostname, selected_browser_name)
        self.result = selected_browser, self.url
        self.root.destroy()

    def run(self):
        """Run the application."""
        self.root.mainloop()
        return self.result


class CustomButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            bg="white",
            fg="black",
            bd=2,
            relief="solid",
            activeforeground="black",
            padx=10,
            pady=5,
            cursor="hand2",
        )


class CustomCheckbutton(tk.Checkbutton):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            bg="white",
            cursor="hand2",
            indicatoron=20,
        )
