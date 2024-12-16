from sqlalchemy import Column, Integer, String, Float
from dal.database import Base
from sqlalchemy.orm import relationship
# from models.tracking_record import TrackingRecord

class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    location_name = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    ecosystem_type = Column(String(50), nullable=True)

    # Relationship to other tables
    tracking_records = relationship("TrackingRecord", back_populates="location")
