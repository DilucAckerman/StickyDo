# Central place to tune StickyDo's look. Change a number, restart the app.

WINDOW_OPACITY = 0.45     # 0 = fully see-through, 1 = fully solid
TILE_OPACITY = 0.14       # kept HIGHER than WINDOW_OPACITY so tiles stand out
DIVIDER_OPACITY = 0.25    # thin white separator lines
HOVER_OPACITY = 0.10

FONT_STACK = '"Sulfur Point", "Comfortaa", "Quicksand", sans-serif'


def build_css():
    return f"""
window {{
    background-color: rgba(20, 18, 24, {WINDOW_OPACITY});
    border-radius: 14px;
    color: #f5f2f6;
    font-family: {FONT_STACK};
}}

/* ---- Nav bar ---- */
box.navbar {{
    background: transparent;
    padding: 8px 12px;
    margin: 10px 10px 0 10px;
    border-bottom: 1px solid rgba(255, 255, 255, {DIVIDER_OPACITY});
}}

/* ---- Notes / Todos tab switcher ---- */
stackswitcher {{
    background: transparent;
}}

stackswitcher button {{
    background: transparent;
    padding: 4px 14px;
    color: rgba(245, 242, 246, 0.55);
    font-family: {FONT_STACK};
}}

stackswitcher button:not(:last-child) {{
    border-right: 1px solid rgba(255, 255, 255, {DIVIDER_OPACITY});
}}

stackswitcher button:checked {{
    color: #ffffff;
}}

/* ---- Close button ---- */
button.close-btn {{
    background: transparent;
    color: rgba(245, 242, 246, 0.5);
    border-radius: 6px;
    padding: 2px 8px;
}}

button.close-btn:hover {{
    background-color: rgba(224, 95, 111, 0.5);
    color: #ffffff;
}}

/* ---- General buttons act as tiles too ---- */
button {{
    background-color: rgba(255, 255, 255, {TILE_OPACITY});
    border-radius: 8px;
    padding: 4px 10px;
}}

button:hover {{
    background-color: rgba(255, 255, 255, {TILE_OPACITY + HOVER_OPACITY});
}}

button.close-btn:hover {{
    background-color: rgba(224, 95, 111, 0.5);
}}

/* ---- Entry fields ---- */
entry {{
    background-color: rgba(255, 255, 255, {TILE_OPACITY});
    border-radius: 8px;
    padding: 6px 10px;
    border: 1px solid rgba(255, 255, 255, {DIVIDER_OPACITY});
    color: #f5f2f6;
}}

entry:focus-within {{
    border-color: rgba(255, 255, 255, 0.45);
}}

/* ---- Note / todo tiles ---- */
row {{
    background-color: rgba(255, 255, 255, {TILE_OPACITY});
    border-radius: 10px;
    padding: 8px;
    margin: 4px 10px;
}}

row:hover {{
    background-color: rgba(255, 255, 255, {TILE_OPACITY + HOVER_OPACITY});
}}

/* ---- Overdue / caption text ---- */
label.error {{
    color: #e05f6f;
}}

label.caption {{
    color: rgba(245, 242, 246, 0.45);
    font-size: 0.85em;
}}

label.resize-handle {{
    color: rgba(245, 242, 246, 0.35);
}}

scrolledwindow, viewport, list, stack {{
    background: transparent;
    background-color: transparent;
}}
"""