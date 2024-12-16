from sqlalchemy import Column, Integer, String, Enum
from dal.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum("Admin", "Marine Biologist", "Environmental Agency", "Research Institution"), nullable=False)
