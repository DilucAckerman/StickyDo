import sqlite3
import os

DB_DIR = os.path.expanduser("~/.local/share/stickydo")
DB_PATH = os.path.join(DB_DIR, "stickydo.db")

def get_connection():
    os.makedirs(DB_DIR, exist_ok = True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            color TEXT DEFAULT 'yellow',
            x INTEGER DEFAULT 100,
            y INTEGER DEFAULT 100,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            done INTEGER DEFAULT 0,
            due_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn

# ---- Notes CRUD ----

def add_note(content="",x=100,y=100):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO notes (content, x, y) Values (?, ?, ?)",(content,x,y)
    )
    conn.commit()
    note_id = cur.lastrowid
    conn.close()
    return note_id

def get_all_notes():
    conn = get_connection()
    rows = conn.execute("SELECT id, content, color, x, y FROM notes").fetchall()
    conn.close()
    return rows

def update_note_content(note_id,content):
    conn = get_connection()
    conn.execute("UPDATE notes SET content = ? WHERE id = ?", (content, note_id))
    conn.commit()
    conn.close()

def delete_note(note_id):
    conn = get_connection()
    conn.execute("DELETE FROM notes WHERE id = ?",(note_id,))
    conn.commit()
    conn.close()

# ---- Todos CRUD ----

def add_todo(task):
    conn = get_connection()
    cur = conn.execute("INSERT INTO todos (task) VALUES (?)",(task,))
    conn.commit()
    todo_id = cur.lastrowid
    conn.close()
    return todo_id

def get_all_todos():
    conn = get_connection()
    rows = conn.execute("SELECT id,task,done,due_date FROM todos").fetchall()
    conn.close()
    return rows

def toggle_todo_done(todo_id):
    conn = get_connection()
    conn.execute("UPDATE todos SET done = NOT done WHERE id = ?",(todo_id,))
    conn.commit()
    conn.close()

def delete_todo(todo_id):
    conn = get_connection()
    conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    