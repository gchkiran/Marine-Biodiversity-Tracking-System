from sqlalchemy import Column, Integer, String, Float, ForeignKey
from dal.database import Base

class PollutionSource(Base):
    __tablename__ = 'pollution_source'

    id = Column(Integer, primary_key=True)
    pollution_source_name = Column(String(100), nullable=False)
    source_type = Column(String(100), nullable=False)
    pollutant_level = Column(Float)
    location_id = Column(Integer, ForeignKey('location.id'))
