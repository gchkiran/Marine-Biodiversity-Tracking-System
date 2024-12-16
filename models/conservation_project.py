from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from dal.database import Base
from models.relationships.project_organization import ProjectOrganization
from models.organization import Organization
from models.conservation_effort import ConservationEffort

class ConservationProject(Base):
    __tablename__ = 'conservation_project'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    goal = Column(String(255))

    organizations = relationship("Organization", secondary="project_organization", back_populates="projects")
    efforts = relationship("ConservationEffort", back_populates="project")
