# provider/serverA.py
import json
from types import SimpleNamespace
from fastapi import FastAPI, Request, HTTPException
import uvicorn, requests

from agents import function_tool  # ← 你的 SDK

# 1) 直接定义 FunctionTool（不再取 __wrapped__）
@function_tool
def add(x: int, y: int) -> int:
    "return the sum of x and y"
    return x + y

app = FastAPI()

# 用 FunctionTool 本体做注册表
REGISTRY = {"add": add}

# 2) 执行端点：把 JSON 透传给 FunctionTool.on_invoke_tool
@app.post("/remote/run/{slug}")
async def run(slug: str, request: Request):
    tool = REGISTRY.get(slug)
    if not tool:
        raise HTTPException(404, "unknown tool")
    payload = await request.json()
    # 最小上下文占位；大多数工具不依赖它
    ctx = SimpleNamespace()
    # on_invoke_tool 接受 JSON 字符串参数
    result = await tool.on_invoke_tool(ctx, json.dumps(payload))
    # 统一包一层，保持返回结构清晰
    return {"output": result}

def push_to_B(consumer_base="http://localhost:8200"):
    """把元数据（name/desc/schema + endpoint）推到 B"""
    meta = {
        "slug": "add",
        "name": add.name,
        "description": add.description or "",
        "params_json_schema": add.params_json_schema,
        "endpoint_url": "http://localhost:8100/remote/run/add",
    }
    r = requests.post(f"{consumer_base}/remote/register", json=meta, timeout=5)
    r.raise_for_status()
    print("Pushed meta to B:", r.json())

if __name__ == "__main__":
    # 启动服务；如果 B 未起，推送可能失败，等 B 起后再调 push_to_B 即可
    import threading, time
    def serve():
        uvicorn.run(app, host="0.0.0.0", port=8100, log_level="warning")
    t = threading.Thread(target=serve, daemon=True)
    t.start()
    time.sleep(0.5)
    try:
        push_to_B()
    except Exception as e:
        print("Push failed (start B then retry):", e)
    t.join()
