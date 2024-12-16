from sqlalchemy import Column, Integer, Float, Date, ForeignKey, String
from dal.database import Base

class SpeciesHealthData(Base):
    __tablename__ = 'species_health_data'

    id = Column(Integer, primary_key=True)
    health_metric = Column(String(100), nullable=False)
    value = Column(Float)
    date_recorded = Column(Date)
    species_id = Column(Integer, ForeignKey('species.id'))
