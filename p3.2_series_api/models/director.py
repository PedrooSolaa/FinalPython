from sqlalchemy import Column, Integer, String
from database.database import Base

class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    edad = Column(Integer, nullable=False)
    lugar_nacimiento = Column(String, nullable=False)