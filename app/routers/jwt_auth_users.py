from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext

ALGORITHM = 'HS256'
ACCESS_TOKEN_DURATION = 1
SECRET = 'b6241a6e9171ad401a33af0466890b419febb5df081aa4604940c7ebe6b33ee0'

router = APIRouter(prefix="/jwt", tags=["jwt auth users"])

oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

crypt = CryptContext(schemes=['bcrypt'])

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
        "password": "$2a$12$TVMm1fgGtAvFdkYAwAKRE.cSbkOVBw6.4Xd09Kw52Qi1i/y4pYzK2"
    },
    "manijas2": {
        "username": "manijas2",
        "full_name": "Manuel Moreno2",
        "email": "zerocool2.moreno@gmail.com",
        "disabled": True,
        "password": "$2a$12$yR1kcB1nm7fzbxoti7ATW.dKlMf6P20xYuLudSQ.11KGfIngA.tku"
    }
}

async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get('sub')

        if username is None:
            raise exception

    except JWTError:
        raise exception
    return search_user(username)


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

async def current_user(user: User = Depends(auth_user)):
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

    if not crypt.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")

    access_token = {
        'sub': user.username,
        'exp': datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(user: User = Depends(current_user)):
    return user
