import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gtk4LayerShell', '1.0')
from gi.repository import Gtk, Gtk4LayerShell as LayerShell

from stickydo.db import (
    get_all_notes, add_note, update_note_content,
    get_all_todos, add_todo, toggle_todo_done, delete_todo
)


def create_main_window(app):
    win = Gtk.ApplicationWindow(application=app)
    win.set_decorated(False)
    win.set_default_size(300, 400)

    LayerShell.init_for_window(win)
    LayerShell.set_layer(win, LayerShell.Layer.BOTTOM)
    LayerShell.set_anchor(win, LayerShell.Edge.TOP, True)
    LayerShell.set_anchor(win, LayerShell.Edge.LEFT, True)
    LayerShell.set_margin(win, LayerShell.Edge.TOP, 100)
    LayerShell.set_margin(win, LayerShell.Edge.LEFT, 100)
    LayerShell.set_keyboard_mode(win, LayerShell.KeyboardMode.ON_DEMAND)

    # Tracks current position/size manually, since layer-shell has no getters
    state = {"x": 100, "y": 100, "w": 300, "h": 400}

    outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

    # ---------------- Nav bar ----------------
    navbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
    navbar.set_margin_top(6)
    navbar.set_margin_bottom(6)
    navbar.set_margin_start(6)
    navbar.set_margin_end(6)

    stack = Gtk.Stack()
    stack.set_vexpand(True)
    switcher = Gtk.StackSwitcher()
    switcher.set_stack(stack)

    close_button = Gtk.Button(label="✕")
    close_button.connect("clicked", lambda b: win.close())

    navbar.append(switcher)
    spacer = Gtk.Box()
    spacer.set_hexpand(True)
    navbar.append(spacer)
    navbar.append(close_button)

    # Drag-to-move: attached to the navbar (excluding button hitboxes mostly)
    move_gesture = Gtk.GestureDrag()

    def on_move_update(gesture, offset_x, offset_y):
        new_x = int(state["x"] + offset_x)
        new_y = int(state["y"] + offset_y)
        LayerShell.set_margin(win, LayerShell.Edge.LEFT, new_x)
        LayerShell.set_margin(win, LayerShell.Edge.TOP, new_y)

    def on_move_end(gesture, offset_x, offset_y):
        state["x"] += int(offset_x)
        state["y"] += int(offset_y)

    move_gesture.connect("drag-update", on_move_update)
    move_gesture.connect("drag-end", on_move_end)
    navbar.add_controller(move_gesture)

    outer.append(navbar)
    outer.append(stack)

    # ---------------- Notes page ----------------
    notes_page = build_notes_page()
    stack.add_titled(notes_page, "notes", "Notes")

    # ---------------- Todos page ----------------
    todos_page = build_todos_page()
    stack.add_titled(todos_page, "todos", "Todos")

    # ---------------- Resize handle ----------------
    resize_handle = Gtk.Label(label="◢")
    resize_handle.set_halign(Gtk.Align.END)
    resize_handle.set_valign(Gtk.Align.END)
    resize_handle.set_margin_end(4)
    resize_handle.set_margin_bottom(4)

    resize_gesture = Gtk.GestureDrag()

    def on_resize_update(gesture, offset_x, offset_y):
        new_w = max(200, int(state["w"] + offset_x))
        new_h = max(200, int(state["h"] + offset_y))
        win.set_default_size(new_w, new_h)

    def on_resize_end(gesture, offset_x, offset_y):
        state["w"] = max(200, int(state["w"] + offset_x))
        state["h"] = max(200, int(state["h"] + offset_y))

    resize_gesture.connect("drag-update", on_resize_update)
    resize_gesture.connect("drag-end", on_resize_end)
    resize_handle.add_controller(resize_gesture)

    overlay = Gtk.Overlay()
    overlay.set_child(outer)
    overlay.add_overlay(resize_handle)

    win.set_child(overlay)
    return win


# ==================== Notes page ====================

def build_notes_page():
    notes_stack = Gtk.Stack()  # switches between list view and editor view

    list_box_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    list_box_container.set_margin_top(6)
    list_box_container.set_margin_start(6)
    list_box_container.set_margin_end(6)

    add_btn = Gtk.Button(label="+ New Note")
    list_box_container.append(add_btn)

    scrolled = Gtk.ScrolledWindow()
    scrolled.set_vexpand(True)
    listbox = Gtk.ListBox()
    scrolled.set_child(listbox)
    list_box_container.append(scrolled)

    editor_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    editor_container.set_margin_top(6)
    editor_container.set_margin_start(6)
    editor_container.set_margin_end(6)

    back_btn = Gtk.Button(label="← Back")
    editor_container.append(back_btn)

    editor_scrolled = Gtk.ScrolledWindow()
    editor_scrolled.set_vexpand(True)
    textview = Gtk.TextView()
    textview.set_wrap_mode(Gtk.WrapMode.WORD)
    editor_scrolled.set_child(textview)
    editor_container.append(editor_scrolled)

    notes_stack.add_named(list_box_container, "list")
    notes_stack.add_named(editor_container, "editor")

    current_note_id = {"id": None}

    def refresh_notes_list():
        child = listbox.get_first_child()
        while child:
            nxt = child.get_next_sibling()
            listbox.remove(child)
            child = nxt

        for note_id, content, color, x, y in get_all_notes():
            preview = (content[:30] + "...") if len(content) > 30 else content
            preview = preview or "(empty note)"
            row_label = Gtk.Label(label=preview)
            row_label.set_xalign(0)
            row_label.set_margin_top(4)
            row_label.set_margin_bottom(4)
            row_label.set_margin_start(6)

            row = Gtk.ListBoxRow()
            row.set_child(row_label)
            row.note_id = note_id  # stash id directly on the row widget
            listbox.append(row)

    def open_editor(note_id, content):
        current_note_id["id"] = note_id
        textview.get_buffer().set_text(content)
        notes_stack.set_visible_child_name("editor")

    def on_row_activated(box, row):
        notes = dict((n[0], n[1]) for n in get_all_notes())
        open_editor(row.note_id, notes.get(row.note_id, ""))

    listbox.connect("row-activated", on_row_activated)

    def on_back_clicked(btn):
        # Save happens live via buffer "changed" below, just navigate back
        refresh_notes_list()
        notes_stack.set_visible_child_name("list")

    back_btn.connect("clicked", on_back_clicked)

    def on_buffer_changed(buf):
        if current_note_id["id"] is not None:
            start, end = buf.get_bounds()
            text = buf.get_text(start, end, False)
            update_note_content(current_note_id["id"], text)

    textview.get_buffer().connect("changed", on_buffer_changed)

    def on_add_clicked(btn):
        note_id = add_note("")
        open_editor(note_id, "")

    add_btn.connect("clicked", on_add_clicked)

    refresh_notes_list()
    notes_stack.set_visible_child_name("list")
    return notes_stack


# ==================== Todos page ====================

def build_todos_page():
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    box.set_margin_top(6)
    box.set_margin_start(6)
    box.set_margin_end(6)

    entry_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    entry = Gtk.Entry()
    entry.set_hexpand(True)
    entry.set_placeholder_text("New task...")
    add_button = Gtk.Button(label="Add")
    entry_row.append(entry)
    entry_row.append(add_button)
    box.append(entry_row)

    scrolled = Gtk.ScrolledWindow()
    scrolled.set_vexpand(True)
    listbox = Gtk.ListBox()
    scrolled.set_child(listbox)
    box.append(scrolled)

    def refresh_list():
        child = listbox.get_first_child()
        while child:
            nxt = child.get_next_sibling()
            listbox.remove(child)
            child = nxt

        for todo_id, task, done, due_date in get_all_todos():
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            checkbox = Gtk.CheckButton()
            checkbox.set_active(bool(done))

            def on_toggle(cb, tid=todo_id):
                toggle_todo_done(tid)
                refresh_list()
            checkbox.connect("toggled", on_toggle)

            label = Gtk.Label(label=task)
            label.set_hexpand(True)
            label.set_xalign(0)
            if done:
                label.set_opacity(0.5)

            delete_button = Gtk.Button(label="✕")
            def on_delete(btn, tid=todo_id):
                delete_todo(tid)
                refresh_list()
            delete_button.connect("clicked", on_delete)

            row.append(checkbox)
            row.append(label)
            row.append(delete_button)
            listbox.append(row)

    def on_add_clicked(btn):
        task = entry.get_text().strip()
        if task:
            add_todo(task)
            entry.set_text("")
            refresh_list()

    add_button.connect("clicked", on_add_clicked)
    entry.connect("activate", on_add_clicked)

    refresh_list()
    return box