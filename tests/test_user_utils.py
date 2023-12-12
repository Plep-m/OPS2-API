from src.user_utils import create_user
from src.database import SessionLocal
from models.user_model import GenderEnum

def test_create_user_ko():
  with SessionLocal() as db:
     try:
      create_user(db, "TonyTony", "Chopper", GenderEnum.MALE, "+983456234", "45665", "456 Elm St", "Tokyo", "Japan", ["notarole"])
     except Exception as e:
      assert str(e) == "The specified roles were not found in the database."

def test_create_user_ko_2():
  with SessionLocal() as db:
    try:
      create_user(db, "Nagisa", "Shiota", GenderEnum.NEUTRAL, "+983456734", "45665", "456 Elm St", "Tokyo", "Japan")
    except Exception as e:
      assert str(e) == "Nagisa Shiota already exist"
