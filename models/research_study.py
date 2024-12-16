from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from dal.database import Base
from models.relationships.study_researcher import StudyResearcher
from models.researcher import Researcher

class ResearchStudy(Base):
    __tablename__ = 'research_study'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    published_date = Column(Date)

    researchers = relationship("Researcher", secondary="study_researcher", back_populates="studies")
