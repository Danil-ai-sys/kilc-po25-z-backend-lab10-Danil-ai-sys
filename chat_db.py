"""The chat from Python: the same SQL, with ? marks."""
import sqlite3

DB = "chat.db"


def connect(path: str = DB) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def add_user(conn: sqlite3.Connection, name: str) -> int:
    cursor = conn.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()
    return cursor.lastrowid


def add_message(conn: sqlite3.Connection, room_id: int, user_id: int, text: str) -> int:
    cursor = conn.execute(
        "INSERT INTO messages (room_id, user_id, text) VALUES (?, ?, ?)",
        (room_id, user_id, text),
    )
    conn.commit()
    return cursor.lastrowid


def find_user(conn: sqlite3.Connection, name: str) -> tuple | None:
    return conn.execute("SELECT id, name FROM users WHERE name = ?", (name,)).fetchone()


def find_messages(
    conn: sqlite3.Connection,
    room_id: int,
    user_id: int | None = None,
    order: str = "asc",
    limit: int = 10,
    offset: int = 0,
) -> list[tuple]:
    # 1. the fixed part, and the values that go with it
    sql = "SELECT id, user_id, text FROM messages WHERE room_id = ?"
    values: list = [room_id]
    # 2. an optional filter
    if user_id is not None:
        sql += " AND user_id = ?"
        values.append(user_id)
    # 3. the order: DESC is a word of SQL, not a value, so it is chosen with an if
    if order == "desc":
        sql += " ORDER BY id DESC"
    else:
        sql += " ORDER BY id ASC"
    # 4. the page
    sql += " LIMIT ? OFFSET ?"
    values += [limit, offset]
    return conn.execute(sql, values).fetchall()
