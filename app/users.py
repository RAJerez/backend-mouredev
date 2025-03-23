from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Inicia el server: uvicorn users:app --reload

app = FastAPI()


# Creamos nuestro objeto de modelo de la Entidad User

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


# Base de datos ficticia

users_list = [User(id=1, name="Brais", surname="Moure", url="https://moure.dev", age=35),
              User(id=2, name="Moure", surname="Dev", url="https://mouredev.com", age=36),
              User(id=3, name="Brais", surname="Dahlberg", url="https://haakon.com", age=37)]


# OPERACIONES GET

@app.get("/usersjson")
async def usersjson():
    return [{"name": "Brais", "surname": "Moure", "url": "https//:moure.dev", "age": 35},
            {"name": "Moure", "surname": "Dev", "url": "https://mouredev.com", "age": 36},
            {"name": "Haakon", "surname": "Dahlberg", "url": "https//haakon.com", "age": 37}]


@app.get("/users")
async def users():
    return users_list

# PATH
# Se puede usar cuando se trata de un PARAMETRO OBLIGATORIO
# Ejemplo de parametros que pueden ir por el PATH de la URL --> "/user/{id}"

@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)
    

# QUERY
# Se puede usar cuando se trata de un PARAMETRO OPCIONAL
# Ejemplo de parametros que pueden ir por la QUERY --> "/user/{id}"
# Asi podemos comenzar a igualar una clave a un valor dentro de la URL
# http://127.0.0.1:8000/user/?id=1&name=Brais

@app.get("/user/")
async def user(id: int, name: str):
    return search_user(id)



# OPERACIONES POST

@app.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    users_list.append(user)
    return user



# OPERACIONES PUT
@app.put("/user/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    
    if not found:
        return {"error": "No se ha actualizado el usuario"}
    else:
        return user


# OPERACIONES DELETE

@app.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    
    if not found:
        return {"error": "No se ha eliminado el usuario"}








# OPERACIONES NO EXPUESTAS EN LA API
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}
    