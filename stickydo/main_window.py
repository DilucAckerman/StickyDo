import gi
import os
import cairo
gi.require_version('Gtk', '4.0')
gi.require_version('Gtk4LayerShell', '1.0')
from gi.repository import Gtk, Gtk4LayerShell as LayerShell
from stickydo.theme import WINDOW_RADIUS
from datetime import date
from stickydo.db import (
    get_all_notes, add_note, update_note_content, delete_note,
    get_all_todos, add_todo, toggle_todo_done, delete_todo, update_todo_time
)

def create_main_window(app):
    win = Gtk.ApplicationWindow(application=app)
    win.set_decorated(False)
    win.set_default_size(300, 400)

    LayerShell.init_for_window(win)
    LayerShell.set_namespace(win, "stickydo")
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
    navbar.add_css_class("navbar")
    navbar.set_margin_top(6)
    navbar.set_margin_bottom(6)
    navbar.set_margin_start(6)
    navbar.set_margin_end(6)

    stack = Gtk.Stack()
    stack.set_vexpand(True)

    notes_btn = Gtk.ToggleButton(label="Notes")
    todos_btn = Gtk.ToggleButton(label="Todos")
    notes_btn.add_css_class("tab-btn")
    todos_btn.add_css_class("tab-btn")
    notes_btn.set_active(True)

    tab_separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
    tab_separator.add_css_class("tab-divider")

    def on_notes_toggled(btn):
        if btn.get_active():
            todos_btn.set_active(False)
            stack.set_visible_child_name("notes")

    def on_todos_toggled(btn):
        if btn.get_active():
            notes_btn.set_active(False)
            stack.set_visible_child_name("todos")

    notes_btn.connect("toggled", on_notes_toggled)
    todos_btn.connect("toggled", on_todos_toggled)

    switcher = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    switcher.append(notes_btn)
    switcher.append(tab_separator)
    switcher.append(todos_btn)

    close_button = Gtk.Button(label="✕")
    close_button.add_css_class("close-btn")
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
   

    def draw_resize_corner(area, cr, width, height):
        pad = 4  # room for the rounded cap to render without clipping
        radius = min(WINDOW_RADIUS, width - pad, height - pad)

        cr.set_line_width(4)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_source_rgba(1, 1, 1, 0.4)
        cr.arc(pad, pad, radius, 0, 1.5708)
        cr.stroke()

    resize_handle = Gtk.DrawingArea()
    resize_handle.set_content_width(WINDOW_RADIUS+6)
    resize_handle.set_content_height(WINDOW_RADIUS+6)
    resize_handle.set_draw_func(draw_resize_corner)
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
    list_box_container.set_margin_start(14)
    list_box_container.set_margin_end(14)

    add_btn = Gtk.Button(label="+ New Note")
    list_box_container.append(add_btn)

    scrolled = Gtk.ScrolledWindow()
    scrolled.set_vexpand(True)
    listbox = Gtk.ListBox()
    scrolled.set_child(listbox)
    list_box_container.append(scrolled)

    editor_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    editor_container.set_margin_top(6)
    editor_container.set_margin_start(14)
    editor_container.set_margin_end(14)

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

            row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            row_label = Gtk.Label(label=preview)
            row_label.set_xalign(0)
            row_label.set_hexpand(True)
            row_label.set_margin_top(4)
            row_label.set_margin_bottom(4)
            row_label.set_margin_start(6)

            delete_btn = Gtk.Button(label="✕")
            def on_delete(btn, nid=note_id):
                delete_note(nid)
                refresh_notes_list()
            delete_btn.connect("clicked", on_delete)

            row_box.append(row_label)
            row_box.append(delete_btn)

            row = Gtk.ListBoxRow()
            row.set_child(row_box)
            row.note_id = note_id
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
    box.set_margin_bottom(14)
    box.set_margin_start(14)
    box.set_margin_end(14)

    entry_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    entry = Gtk.Entry()
    entry.set_hexpand(True)
    entry.set_placeholder_text("New task...")

    selected_time = {"start": None, "end": None}

    clock_icon_path = os.path.join(os.path.dirname(__file__), "assets", "icons", "clock.png")
    time_icon = Gtk.Image.new_from_file(clock_icon_path)
    time_icon.set_pixel_size(24)
    time_button = Gtk.MenuButton()
    time_button.set_child(time_icon)

    # --- Time picker popover ---
    popover = Gtk.Popover()
    picker_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    picker_box.set_margin_top(10)
    picker_box.set_margin_bottom(10)
    picker_box.set_margin_start(10)
    picker_box.set_margin_end(10)

    def make_time_row(label_text):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        label = Gtk.Label(label=label_text)
        label.set_size_request(40, -1)
        label.set_xalign(0)
        hour = Gtk.SpinButton.new_with_range(0, 23, 1)
        hour.set_value(9)
        minute = Gtk.SpinButton.new_with_range(0, 55, 5)
        minute.set_value(0)
        row.append(label)
        row.append(hour)
        row.append(Gtk.Label(label=":"))
        row.append(minute)
        return row, hour, minute

    start_row, start_hour, start_minute = make_time_row("Start")
    end_row, end_hour, end_minute = make_time_row("End")

    confirm_btn = Gtk.Button(label="Set")

    def on_confirm(btn):
        s = f"{int(start_hour.get_value()):02d}:{int(start_minute.get_value()):02d}"
        e = f"{int(end_hour.get_value()):02d}:{int(end_minute.get_value()):02d}"
        selected_time["start"] = s
        selected_time["end"] = e
        popover.popdown()

    confirm_btn.connect("clicked", on_confirm)

    picker_box.append(start_row)
    picker_box.append(end_row)
    picker_box.append(confirm_btn)
    popover.set_child(picker_box)
    time_button.set_popover(popover)

    add_button = Gtk.Button(label="Add")
    entry_row.append(entry)
    entry_row.append(time_button)
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

        for todo_id, task, done, start_time, end_time in get_all_todos():
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

            checkmark_icon_path = os.path.join(os.path.dirname(__file__), "assets", "icons", "checkmark.png")
            checkbox = Gtk.ToggleButton()
            checkbox.add_css_class("custom-checkbox")
            checkbox.set_active(bool(done))
            check_image = Gtk.Image.new_from_file(checkmark_icon_path)
            check_image.set_pixel_size(18)
            check_image.set_opacity(1.0 if done else 0.0)
            checkbox.set_child(check_image)

            def on_toggle(cb, tid=todo_id, img=check_image):
                toggle_todo_done(tid)
                img.set_opacity(1.0 if cb.get_active() else 0.0)
                refresh_list()
            checkbox.connect("toggled", on_toggle)

            text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            label = Gtk.Label(label=task)
            label.set_hexpand(True)
            label.set_xalign(0)
            if done:
                label.set_opacity(0.5)
            text_box.append(label)

            if start_time and end_time:
                time_label = Gtk.Label(label=f"{start_time} - {end_time}")
                time_label.set_xalign(0)
                time_label.add_css_class("caption")
                text_box.append(time_label)

            delete_button = Gtk.Button(label="✕")
            def on_delete(btn, tid=todo_id):
                delete_todo(tid)
                refresh_list()
            delete_button.connect("clicked", on_delete)

            row.append(checkbox)
            row.append(text_box)
            row.append(delete_button)
            listbox.append(row)

    def on_add_clicked(btn):
        task = entry.get_text().strip()
        if task:
            add_todo(task, selected_time["start"], selected_time["end"])
            entry.set_text("")
            selected_time["start"] = None
            selected_time["end"] = None
            refresh_list()

    add_button.connect("clicked", on_add_clicked)
    entry.connect("activate", on_add_clicked)

    refresh_list()
    return box