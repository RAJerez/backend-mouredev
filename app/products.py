from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


@app.get("/products")
async def products():
    return ["Producto 1", "Producto 2", "Producto 3", "Producto 4", "Producto 5"]