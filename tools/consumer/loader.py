# tools/consumer/loader.py
import json
import requests
from typing import Optional, Dict, Any

from agents import function_tool, FunctionTool  # 按你的 SDK 实际路径导入
from consumer.consumer_db import get_tool_row


def load_function(
    *,
    tool_id: Optional[int] = None,
    slug: Optional[str] = None,
    db_path: str = "./tools.db",
) -> FunctionTool:
    """
    从数据库加载工具元数据，并生成一个“API 代理工具”：
    - 该工具的 schema（参数名/必填/描述）来自 DB；
    - 实际执行会 POST JSON 到保存的 endpoint_url。

    返回：FunctionTool
    """
    assert tool_id or slug, "tool_id 或 slug 必填一个"

    # 读取元数据
    name, description, schema_json, endpoint_url = get_tool_row(
        tool_id=tool_id, slug=slug
    )
    schema: Dict[str, Any] = json.loads(schema_json)

    # 代理函数：**kwargs → POST 到 endpoint_url
    def _proxy(**kwargs):
        r = requests.post(endpoint_url, json=kwargs, timeout=10)
        r.raise_for_status()
        try:
            return r.json()
        except Exception:
            return r.text

    # 用 @function_tool 包装为工具
    # 注意：这里使用 strict_mode=False，因为 _proxy 使用 **kwargs，
    # 装饰器自动推断会是宽松 schema（additionalProperties=true）。
    # 随后我们会把 DB 中的“严格 schema”覆盖回去。
    tool = function_tool(
        name_override=name,
        description_override=description or f"Proxy tool calling {endpoint_url}",
        strict_mode=False,               # 关键修改：允许宽松 schema
        failure_error_function=None,     # 调试期：出错直接 raise，便于看堆栈
    )(_proxy)

    # 覆盖成 DB 中保存的严格 schema（LLM 将看到这一份）
    try:
        tool.params_json_schema = schema
    except Exception:
        pass

    return tool
