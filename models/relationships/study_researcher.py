from sqlalchemy import Column, Integer, ForeignKey
from dal.database import Base

class StudyResearcher(Base):
    __tablename__ = 'study_researcher'

    study_id = Column(Integer, ForeignKey('research_study.id'), primary_key=True)
    researcher_id = Column(Integer, ForeignKey('researcher.id'), primary_key=True)
