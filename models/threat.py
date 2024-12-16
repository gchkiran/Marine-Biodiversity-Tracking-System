from sqlalchemy import Column, Integer, String, ForeignKey
from dal.database import Base

class Threat(Base):
    __tablename__ = 'threat'

    id = Column(Integer, primary_key=True)
    description = Column(String(255))
    severity = Column(String(50))
    species_id = Column(Integer, ForeignKey('species.id'))
