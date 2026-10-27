# Report, lab 10

Fill this in as you go. Write in your own words.

**Name: Danil Sobar**
**Group: PO 25-Z**
**Date: 27.10.26**

## What works

Tick only what works. "Almost works" is not ticked.

- [x] M1: `schema.sql`, the three tables
- [x] M2: `seed.sql`, six messages
- [x] M3: q1 to q6
- [x] M4: `chat_db.py`
- [x] M5: `injection.py` run, questions answered
- [ ] `pytest`: 29 passed, 0 failed  (run `pytest` yourself and write the real numbers)

## Broken on purpose (M2)

What SQLite said, the last line is enough:

- a message for room 99: `sqlite3.IntegrityError: FOREIGN KEY constraint failed`
- a room with `title` NULL: `sqlite3.IntegrityError: NOT NULL constraint failed: rooms.title`

Which line of `schema.sql` refused each one?

- room 99: `room_id INTEGER NOT NULL REFERENCES rooms (id),` in `messages`. There is no room 99, so the foreign key fails.
- NULL title: `title TEXT NOT NULL` in `rooms`.

## The lists and the tables

| Job | Lab 08: where | Lab 10: what does it |
|---|---|---|
| giving the next id | the counters `next_user_id`, `next_room_id`, `next_id` in `Storage`, with `+= 1` | `id INTEGER PRIMARY KEY`: SQLite counts |
| refusing a second user named Aida | the loop in `add_user` that raises `UserExists` | `name TEXT NOT NULL UNIQUE` |
| refusing a message for a room that does not exist | `self.get_room(room_id)` at the start of `add`, which raises `RoomNotFound` | `room_id ... REFERENCES rooms (id)` (foreign key, with `PRAGMA foreign_keys = ON`) |
| `pinned` is false when not sent | `pinned: bool = False` in the `Message` dataclass | `pinned INTEGER NOT NULL DEFAULT 0` |

## Why ? (M5)

Paste the output of `python injection.py`:

```
'Aida'             unsafe: [(1, 'Aida')]
                   safe:   (1, 'Aida')
'Nobody'           unsafe: []
                   safe:   None
"x' OR '1'='1"     unsafe: [(1, 'Aida'), (2, 'Timur'), (3, 'Dana')]
                   safe:   None
```

1. The f-string makes this SQL text:
   `SELECT id, name FROM users WHERE name = 'x' OR '1'='1'`
   The quote inside the name closes the string early, so the rest is SQL, not data. The condition becomes `name = 'x'` OR `'1'='1'`. The second part is always true, so every row matches.

2. With `O'Brien` the text is `... WHERE name = 'O'Brien'`. The string ends after `O`, and `Brien'` is left over with an unclosed quote. SQLite raises `OperationalError` (syntax error). A real name breaks the unsafe version, even with no attacker.

3. A `?` is bound after the SQL is already parsed, and only as a value (a string or a number). `DESC` is a word of SQL that changes the structure of the query, so it cannot be a value. `ORDER BY ?` with `"DESC"` would sort by the text `'DESC'`, the same for every row. So `DESC` is chosen in Python with an `if`, and only fixed strings that I wrote go into the SQL text.

## Exit task

Write your answers **before** you run anything. Then check them, and fill in the last column. Do not change your first answers.

| Task | My answer | Checked: right or wrong, and why |
|---|---|---|
| A (a) | | |
| A (b) | | |
| A (c) | | |
| A (d) | | |
| B | | |
| C | | |

D:

```sql
```