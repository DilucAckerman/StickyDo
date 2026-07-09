import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio

from stickydo.db import get_all_notes, add_note
from stickydo.note_window import create_note_window


class StickyDoApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.stickydo.app')
        self.note_windows = {}  # note_id -> window, so we can track what's open

    def do_activate(self):
        # Load every saved note and spawn a window for each
        notes = get_all_notes()

        if not notes:
            # First ever run — no notes exist yet, create one to start with
            note_id = add_note("Welcome to StickyDo!")
            notes = get_all_notes()

        for note_id, content, color, x, y in notes:
            self.open_note_window(note_id, content, x, y)

        # New-note shortcut: Ctrl+N
        action = Gio.SimpleAction.new("new_note", None)
        action.connect("activate", self.on_new_note)
        self.add_action(action)
        self.set_accels_for_action("app.new_note", ["<Ctrl>n"])

    def open_note_window(self, note_id, content, x, y):
        win = create_note_window(self, note_id, content, x, y)
        self.note_windows[note_id] = win
        win.present()

    def on_new_note(self, action, param):
        note_id = add_note("")
        self.open_note_window(note_id, "", 100, 100)


if __name__ == "__main__":
    app = StickyDoApp()
    app.run(None)