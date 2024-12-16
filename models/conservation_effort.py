from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from dal.database import Base

class ConservationEffort(Base):
    __tablename__ = 'conservation_effort'

    id = Column(Integer, primary_key=True)
    description = Column(String(255))
    date_started = Column(Date)
    project_id = Column(Integer, ForeignKey('conservation_project.id'))

    project = relationship("ConservationProject", back_populates="efforts")
