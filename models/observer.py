from sqlalchemy import Column, Integer, String
from dal.database import Base

class Observer(Base):
    __tablename__ = 'observer'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    affiliation = Column(String(100))
