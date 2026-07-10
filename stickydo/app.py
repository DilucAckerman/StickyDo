import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from stickydo.main_window import create_main_window


class StickyDoApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.stickydo.app')

    def do_activate(self):
        win = create_main_window(self)
        win.present()


if __name__ == "__main__":
    app = StickyDoApp()
    app.run(None)