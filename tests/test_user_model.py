from datetime import datetime, timedelta
from models.user_model import User

def test_age():
    user = User(birthday=datetime.now() - timedelta(days=20*365))
    assert user.age == 19