from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Datos a nivel Entidad sin contraseña
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

# Datos a nivel Base de Datos con contraseña incluida
class UserDB(User):
    password: str


users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mouredev.com",
        "disabled": False,
        "password":"123456"
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mouredev.com",
        "disabled": True,
        "password":"123457"
    }
}

# Operacion que busca dentro de Base de Datos
def search_user(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

# Creo un criterio de dependencia asincrono
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario inactivo",
                            headers={"WWW-Autenticate": "Bearer"})
    
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Credenciales de autenticacion invalidas",
                            headers={"WWW-Autenticate": "Bearer"})
    
    return user




# OPERACION AUTENTICACION

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="El usuario no es correcto")
    
    user = search_user(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="La contraseña no es correcta")

    return {"access_token": user.username, "token_type": "bearer"}

# OPERACION QUE NOS ENTREGA DATOS DE USUARIOS
# Depende de que el ususario este autenticado

@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user