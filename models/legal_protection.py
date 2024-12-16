from sqlalchemy import Column, Integer, String, Date, ForeignKey
from dal.database import Base

class LegalProtection(Base):
    __tablename__ = 'legal_protection'

    id = Column(Integer, primary_key=True)
    law_name = Column(String(100), nullable=False)
    country = Column(String(50))
    effective_date = Column(Date)
    species_id = Column(Integer, ForeignKey('species.id'))
