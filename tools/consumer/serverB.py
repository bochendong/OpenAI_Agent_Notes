# consumer/serverB.py
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from consumer_db import save_tool_metadata, list_tools
from typing import Optional, Dict, Any

class ToolMeta(BaseModel):
    slug: str
    name: str
    description: Optional[str] = ""
    params_json_schema: Dict[str, Any]
    endpoint_url: str

app = FastAPI()

@app.post("/remote/register")
def remote_register(meta: ToolMeta):
    tool_id = save_tool_metadata(
        slug=meta.slug,
        name=meta.name,
        description=meta.description or "",
        params_json_schema=meta.params_json_schema,
        endpoint_url=meta.endpoint_url,
    )
    return {"ok": True, "tool_id": tool_id}

@app.get("/tools")
def tools():
    return list_tools()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8200, log_level="warning")
