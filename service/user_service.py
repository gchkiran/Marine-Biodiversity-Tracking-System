from sqlalchemy.exc import SQLAlchemyError
from models.user import User
from sqlalchemy import text
from dal.database import get_session
import bcrypt

def get_user_by_username(username):
    session = get_session()
    try:
        return session.query(User).filter_by(username=username).first()
    except SQLAlchemyError as e:
        print(f"Error fetching user: {e}")
    finally:
        session.close()

def validate_user(username, password):
    user = get_user_by_username(username)
    if user and bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
        return user
    return None
