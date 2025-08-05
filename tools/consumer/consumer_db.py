# consumer/consumer_db.py
import sqlite3, time, json, os
from pathlib import Path

DEFAULT_DB = str(Path(__file__).resolve().parents[2] / "tools.db")
DB_PATH = os.environ.get("TOOLS_DB_PATH", DEFAULT_DB)

def _ensure_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
    CREATE TABLE IF NOT EXISTS tools(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      slug TEXT UNIQUE NOT NULL,
      name TEXT NOT NULL,
      description TEXT,
      params_json_schema TEXT NOT NULL,
      endpoint_url TEXT NOT NULL,
      created_at INTEGER NOT NULL,
      updated_at INTEGER NOT NULL
    )""")
    con.commit(); con.close()

def save_tool_metadata(*, slug, name, description, params_json_schema, endpoint_url) -> int:
    _ensure_db()
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT id FROM tools WHERE slug=?", (slug,))
    row = cur.fetchone()
    ts = int(time.time())
    if row:
        tool_id = row[0]
        cur.execute("""UPDATE tools SET
            name=?, description=?, params_json_schema=?, endpoint_url=?, updated_at=?
            WHERE id=?""",
            (name, description, json.dumps(params_json_schema, ensure_ascii=False),
             endpoint_url, ts, tool_id))
    else:
        cur.execute("""INSERT INTO tools
            (slug, name, description, params_json_schema, endpoint_url, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (slug, name, description, json.dumps(params_json_schema, ensure_ascii=False),
             endpoint_url, ts, ts))
        tool_id = cur.lastrowid
    con.commit(); con.close()
    return tool_id

def list_tools():
    _ensure_db()
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT id, slug, name, description, endpoint_url FROM tools ORDER BY id DESC")
    rows = cur.fetchall(); con.close()
    return [{"id": r[0], "slug": r[1], "name": r[2], "description": r[3], "endpoint_url": r[4]} for r in rows]

def get_tool_row(*, tool_id=None, slug=None):
    assert tool_id or slug
    _ensure_db()
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    if tool_id:
        cur.execute("SELECT name, description, params_json_schema, endpoint_url FROM tools WHERE id=?", (tool_id,))
    else:
        cur.execute("SELECT name, description, params_json_schema, endpoint_url FROM tools WHERE slug=?", (slug,))
    row = cur.fetchone(); con.close()
    if not row:
        raise ValueError("tool not found")
    return row
