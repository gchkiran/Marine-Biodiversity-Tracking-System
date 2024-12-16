from sqlalchemy import Column, Integer, String, Float, ForeignKey
from dal.database import Base

class EnvironmentalFactors(Base):
    __tablename__ = 'environmental_factors'

    id = Column(Integer, primary_key=True)
    factor_name = Column(String(100), nullable=False)
    factor_value = Column(Float)
    tracking_record_id = Column(Integer, ForeignKey('tracking_record.id'))
