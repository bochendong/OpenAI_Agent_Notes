import math, threading
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class AddIn(BaseModel):
    x: int
    y: int

class AreaIn(BaseModel):
    radius: float

@app.post("/remote/run/provider-A/add")
def run_add(i: AddIn):
    return {"output": i.x + i.y}

@app.post("/t/provider-A-calculate_area")
def run_area(i: AreaIn):
    return {"output": math.pi * i.radius * i.radius}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8100, log_level="info")