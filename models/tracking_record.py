from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from dal.database import Base
# from models.species import Species 
from models.location import Location


class TrackingRecord(Base):
    __tablename__ = 'tracking_record'

    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    count = Column(Integer, nullable=False)
    species_id = Column(Integer, ForeignKey('species.id'))
    location_id = Column(Integer, ForeignKey('location.id'))

    species = relationship("Species", back_populates="tracking_records")
    location = relationship("Location", back_populates="tracking_records")
