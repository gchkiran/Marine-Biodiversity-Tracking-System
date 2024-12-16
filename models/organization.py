from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from dal.database import Base
from models.relationships.project_organization import ProjectOrganization

class Organization(Base):
    __tablename__ = 'organization'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country = Column(String(50))

    projects = relationship("ConservationProject", secondary="project_organization", back_populates="organizations")
