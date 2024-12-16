from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from dal.database import Base
# from models.species import Species

class Habitat(Base):
    __tablename__ = 'habitat'

    id = Column(Integer, primary_key=True)
    type = Column(String(100), nullable=False)
    description = Column(String(255))
    species_id = Column(Integer, ForeignKey('species.id'))

    species = relationship("Species", back_populates="habitats")
