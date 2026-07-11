import gi
import os
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk, Gio, Gdk
from stickydo.theme import build_css
from stickydo.main_window import create_main_window


class StickyDoApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.stickydo.app')

    def do_activate(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(build_css().encode())
        Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(),
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        win = create_main_window(self)
        win.present()


if __name__ == "__main__":
    app = StickyDoApp()
    app.run(None)