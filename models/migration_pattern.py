from sqlalchemy import Column, Integer, String, ForeignKey
from dal.database import Base

class MigrationPattern(Base):
    __tablename__ = 'migration_pattern'

    id = Column(Integer, primary_key=True)
    description = Column(String(255))
    species_id = Column(Integer, ForeignKey('species.id'))
