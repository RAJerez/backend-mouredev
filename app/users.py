from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get('/users')
async def users():
    return [{"name": "Brais", "surname": "Moure", "url": "https//:moure.dev"},
            {"name": "Agus", "surname": "Jerez", "url": "https//:agus.dev"}]