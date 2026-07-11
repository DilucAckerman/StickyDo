# Central place to tune StickyDo's look. Change a number, restart the app.

WINDOW_TINT = "48, 42, 58" 
WINDOW_OPACITY = 0.45     # 0 = fully see-through, 1 = fully solid
TILE_OPACITY = 0.14       # kept HIGHER than WINDOW_OPACITY so tiles stand out
DIVIDER_OPACITY = 0.25   # thin white separator lines
HOVER_OPACITY = 0.10
BASE_FONT_SIZE = "16px"  # try 15px or 16px if 14 still feels small
WINDOW_RADIUS = 30  # px — also drives the resize handle's curve

FONT_STACK = '"Sulphur Point", "Comfortaa", "Quicksand", sans-serif'


def build_css():
    return f"""
window {{
    background-color: rgba({WINDOW_TINT}, {WINDOW_OPACITY});
    border-radius: {WINDOW_RADIUS}px;
    color: #f5f2f6;
    font-family: {FONT_STACK};
    font-size: {BASE_FONT_SIZE};
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

button {{
    background: transparent;
    border: 1px solid rgba(255, 255, 255, {DIVIDER_OPACITY});
    border-radius: 10px;
    padding: 5px 12px;
    color: rgba(245, 242, 246, 0.75);
}}

button:hover {{
    background-color: rgba(255, 255, 255, {HOVER_OPACITY});
    border-color: rgba(255, 255, 255, 0.4);
    color: #ffffff;
}}

button.tab-btn {{
    background: transparent;
    border: none;
    padding: 4px 14px;
    color: rgba(245, 242, 246, 0.55);
}}

button.tab-btn:hover {{
    background: transparent;
    border: none;
    color: #ffffff;
}}

button.close-btn {{
    background: transparent;
    border: none;
    color: rgba(245, 242, 246, 0.5);
}}

button.close-btn:hover {{
    background-color: rgba(224, 95, 111, 0.35);
    border: none;
    color: #ffffff;
}}

button.custom-checkbox {{
    min-width: 25px;
    min-height: 25px;
    padding: 5px;
    border: 1.5px solid rgba(255, 255, 255, {DIVIDER_OPACITY + 0.15});
    border-radius: 10px;
    background: transparent;
}}

/* ---- Entry fields ---- */
entry {{
    background-color: rgba(255, 255, 255, {TILE_OPACITY});
    border-radius: 10px;
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
    border-radius: 14px;
    padding: 8px;
    margin: 4px 10px;
}}

row label {{
    font-size: 15px;
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

textview, textview text {{
    background-color: transparent;
    color: #f5f2f6;
    caret-color: #f5f2f6;
}}

button.tab-btn {{
    background: transparent;
    padding: 4px 14px;
    color: rgba(245, 242, 246, 0.55);
}}

button.tab-btn:checked {{
    background: transparent;
    color: #ffffff;
}}

separator.tab-divider {{
    background-color: rgba(255, 255, 255, {DIVIDER_OPACITY});
    min-width: 2px;
    margin: 2px 10px;
}}
"""