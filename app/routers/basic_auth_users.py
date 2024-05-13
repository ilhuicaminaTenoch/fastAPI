from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(prefix="/basic-auth", tags=["basic auth authentication"], responses={404: {"description": "Not found"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="/login")


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "manijas": {
        "username": "manijas",
        "full_name": "Manuel Moreno",
        "email": "zerocool.moreno@gmail.com",
        "disabled": False,
        "password": "$Universo01$"
    },
    "manijas2": {
        "username": "manijas2",
        "full_name": "Manuel Moreno2",
        "email": "zerocool2.moreno@gmail.com",
        "disabled": True,
        "password": "$Universo02$"
    }
}


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudieron validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"})
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario inactivo")
    return user


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form_data.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Usuario no es correcto")
    user = search_user_db(form_data.username)
    if form_data.password != user.password:
        raise HTTPException(status_code=400, detail="Contraseña no coincide")
    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(user: User = Depends(current_user)):
    return user
