from datetime import datetime, timedelta
from models.user_model import User

def test_age():
    # Create a User instance with a birthday 20 years ago
    user = User(birthday=datetime.now() - timedelta(days=20*365))

    # Check that the age property returns 20
    assert user.age == 20