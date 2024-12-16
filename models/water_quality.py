from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from dal.database import Base

class WaterQuality(Base):
    __tablename__ = 'water_quality'

    id = Column(Integer, primary_key=True)
    ph_level = Column(Float)
    temperature = Column(Float)
    date_recorded = Column(Date)
    location_id = Column(Integer, ForeignKey('location.id'))
