from sqlalchemy import Column, Integer, ForeignKey
from dal.database import Base

class ProjectOrganization(Base):
    __tablename__ = 'project_organization'

    project_id = Column(Integer, ForeignKey('conservation_project.id'), primary_key=True)
    organization_id = Column(Integer, ForeignKey('organization.id'), primary_key=True)
