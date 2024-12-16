from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from dal.database import Base
from models.relationships.study_researcher import StudyResearcher

class Researcher(Base):
    __tablename__ = 'researcher'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    field_of_study = Column(String(100))

    studies = relationship("ResearchStudy", secondary="study_researcher", back_populates="researchers")
