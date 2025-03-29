from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import products, users, users_db, basic_auth_users, jwt_auth_users


app = FastAPI()

app.include_router(products.router)
app.include_router(users.router)
app.include_router(users_db.router)
# app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/")
async def root():
    return "Hola FastAPI!"

@app.get("/url")
async def url():
    return {"url": "https://mouredev.com/python"}