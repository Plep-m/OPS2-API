import os

from dotenv import load_dotenv

def main_load_env(file_path: str = "ops.env"):
    if os.path.exists(file_path):
        load_dotenv(file_path)
    else :
        print(f'{file_path} not found, using ops_env.env default file')
        load_dotenv('ops_env.env')

main_load_env()
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routes.roles_routes import router as role_router
from routes.users_routes import router as user_router
from routes.tags_routes import router as tag_router
from models.role_model import Base as RoleBase
from models.user_model import Base as UserBase
from models.tag_model import Base as TagBase
from src.database import engine, SessionLocal
from src.role_utils import create_default_roles
from src.user_utils import create_default_users
from src.tag_utils import create_default_tags

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to allow specific origins
    allow_methods=["*"],  # Adjust this to allow specific methods (e.g., ["GET", "POST"])
    allow_headers=["*"],  # Adjust this to allow specific headers
)

app.include_router(role_router, tags=["role"])
app.include_router(user_router, tags=["user"])
app.include_router(tag_router, tags=["tag"])

RoleBase.metadata.create_all(bind=engine)
UserBase.metadata.create_all(bind=engine)
TagBase.metadata.create_all(bind=engine)


with SessionLocal() as db:
    create_default_roles(db)
    create_default_users(db)
    create_default_tags(db)