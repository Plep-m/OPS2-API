from fastapi import APIRouter, Depends, Body, UploadFile, File, HTTPException
from sqlalchemy.orm import Session, joinedload
from fastapi.responses import FileResponse
from src.database import get_db
from models.user_model import User, UserCreate, GenderEnum
from src.user_utils import verify_password
from pathlib import Path
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
import jwt
import os
from src.user_utils import create_user


SECRET_KEY = os.environ.get("SECRET_KEY", "default_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="connect")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_login: str = payload.get("sub")
        if user_login is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    user = db.query(User).filter(User.login == user_login).first()
    if user is None:
        raise credentials_exception
    return user


@router.get("/")
async def hello():
    return {"Hello World !!!"}


@router.get("/verify-token/")
async def verify_token(user: User = Depends(get_current_user)):
    return {"login": user.login}

def get_picture_path(user_login: str, extensions: list, bigExtension=""):
    picture_dir = f"resources/user/profile_picture/{user_login}"
    for ext in extensions:
        picture_path = f"{picture_dir}/{user_login}{bigExtension}.{ext}"
        if os.path.exists(picture_path):
            return picture_path
    return None

def get_picture_for_user(user_login: str, db: Session):
    user = db.query(User).filter(User.login == user_login).first()

    if not user:
        return {"message": "User not found"}

    gender = user.gender
    gender_picture_mapping = {
        GenderEnum.MALE: "resources/basics/man.png",
        GenderEnum.FEMALE: "resources/basics/women.png",
        GenderEnum.NON_BINARY: "resources/basics/unbinary.png"
    }

    if gender in gender_picture_mapping:
        return gender_picture_mapping[gender]
    else:
        return {"message": "Invalid gender"}


@router.get("/users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).options(joinedload(User.roles)).all()
    return users


@router.get("/user/login/{user_login}")
def get_user_by_login(user_login: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.login == user_login).options(joinedload(User.roles)).first()
    return user

@router.get("/user/id/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).options(joinedload(User.roles)).first()
    return user


@router.get("/users/{user_login}/profile_picture/official/")
async def get_profile_picture_official(user_login: str, db: Session = Depends(get_db)):
    extensions = ["png", "jpg", "gif"]
    picture_path = get_picture_path(user_login, extensions, "_official")

    if not picture_path:
        picture_path = get_picture_for_user(user_login, db)
        if isinstance(picture_path, dict):
            return picture_path

    return FileResponse(picture_path)

@router.get("/users/{user_login}/profile_picture/")
async def get_profile_picture(user_login: str, db: Session = Depends(get_db)):
    extensions = ["png", "jpg", "gif"]
    picture_path = get_picture_path(user_login, extensions)

    if not picture_path:
        picture_path = get_picture_for_user(user_login, db)
        if isinstance(picture_path, dict):
            return picture_path

    return FileResponse(picture_path)


@router.post("/users/{user_login}/upload_profile_picture/")
async def upload_profile_picture(
    user_login: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.login == user_login).first()
    if not user:
        return {"message": "User not found"}

    # Ensure the user's profile picture directory exists
    picture_dir = f"resources/user/profile_picture/{user_login}"
    os.makedirs(picture_dir, exist_ok=True)

    # Remove existing profile pictures
    extensions = ["png", "jpg", "gif"]
    for ext in extensions:
        existing_picture_path = f"{picture_dir}/{user_login}.{ext}"
        if os.path.exists(existing_picture_path):
            os.remove(existing_picture_path)

    # Save the uploaded file with the original extension
    original_extension = file.filename.split(".")[-1]
    picture_path = f"{picture_dir}/{user_login}.{original_extension}"
    with open(picture_path, "wb") as f:
        f.write(file.file.read())

    return {"message": "Profile picture uploaded successfully"}

@router.post("/users/{user_login}/upload_profile_picture/official")
async def upload_profile_picture(
    user_login: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.login == user_login).first()
    if not user:
        return {"message": "User not found"}

    # Ensure the user's profile picture directory exists
    picture_dir = f"resources/user/profile_picture/{user_login}"
    os.makedirs(picture_dir, exist_ok=True)

    # Remove existing profile pictures
    extensions = ["png", "jpg", "gif"]
    for ext in extensions:
        existing_picture_path = f"{picture_dir}/{user_login}_official.{ext}"
        if os.path.exists(existing_picture_path):
            os.remove(existing_picture_path)

    # Save the uploaded file with the original extension
    original_extension = file.filename.split(".")[-1]
    picture_path = f"{picture_dir}/{user_login}_official.{original_extension}"
    with open(picture_path, "wb") as f:
        f.write(file.file.read())

    return {"message": "Profile picture uploaded successfully"}

@router.post("/users/")
async def create_new_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    array_roles = []
    for data in user_data.roles:
        array_roles.append(data.name)
    create_user(db, user_data.firstname, user_data.lastname, user_data.gender, user_data.phone, user_data.postal_code, user_data.address, user_data.city, user_data.country, array_roles)
    return {"message": "User created successfully"}
    
@router.post("/connect/")
async def authenticate_user(data: dict = Body(...), db: Session = Depends(get_db)):
    user_login = data.get("user_login")
    password = data.get("password")
    user = db.query(User).filter(User.login == user_login).first()
    
    if not user or verify_password(user, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = {"sub": user.login, "exp": datetime.utcnow() + access_token_expires}
    access_token = jwt.encode(access_token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer"}