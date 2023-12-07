import hashlib
import os
import secrets
from sqlalchemy.orm import Session
from models.user_model import User, GenderEnum
from models.role_model import Role
from unidecode import unidecode
from dotenv import load_dotenv

if os.path.isfile('ops.env'):
    load_dotenv('ops.env')
else:
    print('ops.env not found, using ops_env.env default file')
    load_dotenv('ops_env.env')

def generate_md5(value: str) -> str:
    return hashlib.md5(value.encode()).hexdigest()

def generate_random_password(length: int = 12) -> str:
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#-_*$€£%+=:/;.?<>"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

def verify_password(user, password):
    secret_salt = os.environ.get("SECRET_SALT", "default_salt")
    if (user.password != generate_md5(password + secret_salt)):
        return True
    return False

def create_user(db: Session, firstname: str, lastname: str, gender: GenderEnum, phone: str, postal_code: str, address: str, city: str, country: str, role_names = ["administrator", "staff", "ranger"]):
        # Check if the user already exists
        if db.query(User).filter(User.firstname == unidecode(firstname), User.lastname == unidecode(lastname)).first() is None:
            # Generate the personal token
            secret_salt = os.environ.get("SECRET_SALT", "default_salt")
            user_personnal_token = generate_md5(unidecode(firstname) + unidecode(lastname) + secret_salt)
            
            # Generate a random password and its hash
            random_password = generate_random_password()
            hashed_password = generate_md5(random_password + secret_salt)
            
            # Fetch the roles we want to associate with the user
            roles_to_associate = db.query(Role).filter(Role.name.in_(role_names)).all()

            if not roles_to_associate:
                raise Exception("The specified roles were not found in the database.")

            # Create the user
            db_user = User(
                firstname=unidecode(firstname),
                lastname=unidecode(lastname),
                password=hashed_password, 
                user_personnal_token=user_personnal_token, 
                metas={"fpassword": random_password},
                roles=roles_to_associate,
                gender=gender,
                phone=phone,
                postal_code=postal_code,
                address=address,
                city=city,
                country=country
            )
            
            db.add(db_user)
            db.commit()  # Commit the transaction
        else:
            print(f"{unidecode(firstname)} {unidecode(lastname)} already exist")


# Create users
def create_default_users(db: Session):
    print("Creating default users")
    
    try:
        create_user(db, "Sully", "Natsuya", GenderEnum.MALE, "+123456789", "12345", "123 Main St", "Example City", "Example Country")
        create_user(db, "Éthelle", "Minami", GenderEnum.FEMALE, "+987654321", "54321", "456 Elm St", "Another City", "Different Country")
        db.commit()  # Commit the transaction after both user creations have been attempted
    except Exception as e:
        # Handle exceptions appropriately
        print(f"An error occurred: {e}")
        db.rollback()