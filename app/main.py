from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import products, users


app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")



@app.get("/")
async def root():
    return "Hola FastAPI!"

@app.get("/url")
async def url():
    return {"url": "https://mouredev.com/python"}