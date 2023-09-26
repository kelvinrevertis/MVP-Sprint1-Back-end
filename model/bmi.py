from sqlalchemy import Column, Float, String, Integer
from sqlalchemy.orm import relationship

from model import Base

class BMIData(Base):
    __tablename__ = "bmi_data"

    id = Column("pk_bmi_data", Integer, primary_key=True)
    bmi = Column(Float)
    health = Column(String(50))
    healthy_bmi_range = Column(String(50))

    def __init__(self, bmi, health, healthy_bmi_range):
        self.bmi = bmi
        self.health = health
        self.healthy_bmi_range = healthy_bmi_range
