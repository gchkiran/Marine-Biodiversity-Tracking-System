from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from dal.database import Base
from models.species_interaction import SpeciesInteraction
from models.tracking_record import TrackingRecord
from models.habitat import Habitat


class Species(Base):
    __tablename__ = 'species'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_on = Column(DateTime, nullable=False)
    common_name = Column(String(100), nullable=False)
    scientific_name = Column(String(100), nullable=False)
    conservation_status = Column(String(50), default=None)
    category = Column(String(50), default='Fauna', nullable=False)
    image_url = Column(String(255), default=None)

    # Use string-based reference for the relationship to avoid the InvalidRequestError
    tracking_records = relationship("TrackingRecord", back_populates="species", lazy='joined')
    interactions = relationship("SpeciesInteraction", back_populates="species", lazy='joined')
    habitats = relationship("Habitat", back_populates="species", lazy='joined')
