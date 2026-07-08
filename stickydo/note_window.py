import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gtk4LayerShell','1.0')

from gi.repository import Gtk, Gtk4LayerShell as LayerShell

from stickydo.db import update_note_content

def create_note_window(app,note_id,content,x,y):
    win = Gtk.ApplicationWindow(application=app) #Passing application=app links this window to your Gtk.Application instance
    win.set_default_size(200,200)
    win.set_decorated(False) #No Titlebar

    LayerShell.init_for_window(win) #Actual handshake with Wayland
    LayerShell.set_layer(win, LayerShell.Layer.BOTTOM) #Sets the layer in the background, above wallpaper and below applications
    LayerShell.set_anchor(win, LayerShell.Edge.TOP, True)
    LayerShell.set_anchor(win, LayerShell.Edge.LEFT, True)
    LayerShell.set_margin(win, LayerShell.Edge.TOP, y)
    LayerShell.set_margin(win, LayerShell.Edge.LEFT, x)
    LayerShell.set_keyboard_mode(win, LayerShell.KeyboardMode.ON_DEMAND)

    textview = Gtk.TextView()
    textview.set_wrap_mode(Gtk.WrapMode.WORD) #Acts like a text editor
    buffer = textview.get_buffer()
    buffer.set_text(content)

    def on_text_changed(buf):
        start, end = buf.get_bounds()
        new_text = buf.get_text(start,end,False)
        update_note_content(note_id, new_text)

    buffer.connect("changed", on_text_changed)

    scrolled = Gtk.ScrolledWindow()
    scrolled.set_child(textview)
    win.set_child(scrolled)

    return win
