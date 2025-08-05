import requests

import sqlite3, time, json, re
from typing import Optional, Dict, Any
import requests
from agents import function_tool, FunctionTool  # ← 按你的 SDK 路径导入

DB_PATH = "./tools.db"

# --- 建表 ---
def _ensure_db(db_path: str = DB_PATH):
    con = sqlite3.connect(db_path)
    con.execute("""
    CREATE TABLE IF NOT EXISTS tools (
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

def _now() -> int: return int(time.time())
def _slugify(s: str) -> str:
    s = re.sub(r"\s+", "_", s.strip().lower())
    return re.sub(r"[^a-z0-9_]", "", s)

# --- 保存：传入“已装饰的 FunctionTool” + endpoint ---
def save_function(
    tool: FunctionTool,
    *,
    endpoint_url: str,
    slug: Optional[str] = None,
    db_path: str = DB_PATH,
) -> int:
    _ensure_db(db_path)
    name = getattr(tool, "name", None) or "tool"
    description = getattr(tool, "description", "") or (tool.__doc__ or "")
    params_schema = getattr(tool, "params_json_schema", None)
    if not isinstance(params_schema, dict):
        raise ValueError("The given tool has no params_json_schema; make sure it's a FunctionTool.")
    slug = slug or _slugify(name)

    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT id FROM tools WHERE slug=?", (slug,))
    row = cur.fetchone()
    ts = _now()
    if row:
        tool_id = row[0]
        cur.execute("""UPDATE tools SET
            name=?, description=?, params_json_schema=?, endpoint_url=?, updated_at=?
            WHERE id=?""",
            (name, description, json.dumps(params_schema, ensure_ascii=False),
             endpoint_url, ts, tool_id))
    else:
        cur.execute("""INSERT INTO tools
            (slug, name, description, params_json_schema, endpoint_url, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (slug, name, description, json.dumps(params_schema, ensure_ascii=False),
             endpoint_url, ts, ts))
        tool_id = cur.lastrowid
    con.commit(); con.close()
    return tool_id

# --- 加载：返回一个“API 代理工具”（内部 **kwargs，触发时调用 endpoint）---
def load_function(
    *,
    tool_id: Optional[int] = None,
    slug: Optional[str] = None,
    db_path: str = DB_PATH,
    timeout: float = 10.0,
) -> FunctionTool:
    assert tool_id or slug, "tool_id 或 slug 必填一个"
    _ensure_db(db_path)
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    if tool_id:
        cur.execute("SELECT name, description, params_json_schema, endpoint_url FROM tools WHERE id=?", (tool_id,))
    else:
        cur.execute("SELECT name, description, params_json_schema, endpoint_url FROM tools WHERE slug=?", (slug,))
    row = cur.fetchone(); con.close()
    if not row:
        raise ValueError("Tool not found in DB.")
    name, description, params_schema_json, endpoint_url = row
    saved_schema: Dict[str, Any] = json.loads(params_schema_json)

    # 定义一个“代理函数”——签名使用 **kwargs，更简洁
    def _proxy(**kwargs):
        r = requests.post(endpoint_url, json=kwargs, timeout=timeout)
        r.raise_for_status()
        try:
            return r.json()
        except Exception:
            return r.text

    # 包装为 FunctionTool，并覆盖 schema（让 LLM 知道参数名/必填项/说明）
    tool = function_tool(
        name_override=name,
        description_override=description or f"Proxy tool calling {endpoint_url}",
        strict_mode=True,
        failure_error_function=None,  # 出错直接 raise，便于在 Notebook 调试
    )(_proxy)

    # 覆盖回保存时的 schema（关键：**kwargs 的签名不会自带 schema）
    try:
        tool.params_json_schema = saved_schema
    except Exception:
        pass
    return tool

if __name__ == "__main__":
    print("Testing Regular Tool call")
    print(requests.post(
        "http://localhost:8100/remote/run/provider-A/add",
        json={"x": 3, "y": 4}, timeout=3
    ).json())

    print(requests.post(
        "http://localhost:8100/t/provider-A-calculate_area",
        json={"radius": 3}, timeout=3
    ).json())

    print("Testing Save a Function Tool")

    @function_tool
    def add(x: int, y: int) -> int:
        "return the sum of x and y"
        return x + y
    
    tool_id = save_function(
        add,
        endpoint_url="http://localhost:8100/remote/run/provider-A/add",
        slug="add"
    )
    print("saved tool id:", tool_id)

    print("Testing Load a Function Tool")

    




