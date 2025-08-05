# tools/test_end_to_end.py
import subprocess, sys, time, requests, os, json, asyncio, types
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parent.parent  # 项目根目录
print(ROOT)
PROVIDER = ROOT / "tools" / "provider" / "serverA.py"
CONSUMER = ROOT / "tools" / "consumer" / "serverB.py"

def start(pyfile: Path):
    # 确保以项目根为工作目录，并把根目录加入 PYTHONPATH（防止 import 失败）
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.Popen(
        [sys.executable, str(pyfile)],
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

def wait_http(url, tries=60, delay=0.2):
    for _ in range(tries):
        try:
            requests.get(url, timeout=0.5)
            return
        except Exception:
            time.sleep(delay)
    raise RuntimeError(f"wait_http timeout: {url}")

def drain(prefix, proc):
    """把子进程日志打到控制台，便于看到报错"""
    if proc.stdout:
        for _ in range(50):  # 打印前50行就够定位了；需要更多可调大
            line = proc.stdout.readline()
            if not line:
                break
            print(f"[{prefix}] {line}", end="")

def main():
    # 1) 起 B（consumer）
    b = start(CONSUMER)
    try:
        wait_http("http://localhost:8200/tools")
        print("B up.")
    except Exception:
        print("B failed to start, recent logs:")
        drain("B", b)
        raise

    # 2) 起 A（provider）
    a = start(PROVIDER)
    try:
        wait_http("http://localhost:8100/remote/run/add")
        print("A up.")
    except Exception:
        print("A failed to start, recent logs:")
        drain("A", a)
        raise

    # 3) 补推一次元数据（若 A 启动时 B 未就绪）
    try:
        r = requests.post("http://localhost:8200/remote/register", json={
            "slug": "add",
            "name": "add",
            "description": "return the sum of x and y",
            "params_json_schema": {
                "type":"object",
                "properties":{"x":{"type":"integer"}, "y":{"type":"integer"}},
                "required":["x","y"]
            },
            "endpoint_url":"http://localhost:8100/remote/run/add"
        }, timeout=3)
        if r.status_code == 200:
            print("Pushed meta (retry).")
    except Exception as e:
        print("Push retry failed:", e)

    # 4) 检查 B 是否已保存
    print("B tools:", requests.get("http://localhost:8200/tools").json())

    # 5) 从 B 的 DB 加载代理工具并调用
    sys.path.insert(0, str(ROOT))  # 保险：loader 导入
    from consumer.loader import load_function

    tool = load_function(slug="add")  # 或 tool_id=1

    async def _ainvoke(tool, **kwargs):
        ctx = types.SimpleNamespace()
        import json as _json
        return await tool.on_invoke_tool(ctx, _json.dumps(kwargs))

    res = asyncio.run(_ainvoke(tool, x=3, y=4))
    print("Invocation result:", res)

    # 6) 退出
    a.terminate(); b.terminate()
    drain("A", a); drain("B", b)

if __name__ == "__main__":
    main()
