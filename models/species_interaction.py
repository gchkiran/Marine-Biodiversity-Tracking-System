from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from dal.database import Base

class SpeciesInteraction(Base):
    __tablename__ = 'species_interaction'

    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)
    species_id = Column(Integer, ForeignKey('species.id'))

    species = relationship("Species", back_populates="interactions")