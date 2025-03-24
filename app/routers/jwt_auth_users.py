from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "6ca47231720c54becb030f5b074e6e5efdd08a238a9315e5c285ad71d20e2f4b"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Definiendo un contexto de encriptación
crypt = CryptContext(schemes=["bcrypt"])



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
        "password":"$2a$12$SLofxGsDm7YPh9Y0pNAXIeao5v1NYxIOK8C2J/Ykm316LbjYed3le"
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mouredev.com",
        "disabled": True,
        "password":"$2a$12$Q/.LP9mCQSoSL/aXAQaFHOi0w6nLDqEYuJ3zf5A/tYIAoBAJyknZO"
    }
}

# Operacion que busca dentro de Base de Datos
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    

async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales de autenticación invalidas",
                headers={"WWW-Autenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception
    
    return search_user(username)
        


# Creo un criterio de dependencia asincrono
async def current_user(user: str = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")
    
    return user



# OPERACION AUTENTICACION

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    if not crypt.verify(secret=form.password, hash=user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="La contraseña no es correcta")

    access_token = {
        "sub":user.username,"exp":datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
        }

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}



# OPERACION QUE NOS ENTREGA DATOS DE USUARIOS
# Depende de que el ususario este autenticado

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
