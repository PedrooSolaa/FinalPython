from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class Serie(Base):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    generos = Column(String, nullable=False)  # comma-separated
    puntuacion = Column(Float, nullable=False)
    finalizada = Column(Boolean, nullable=False)
    fecha_estreno = Column(String, nullable=False)
    temporadas = Column(Integer, nullable=False)
    director_id = Column(Integer, ForeignKey('directors.id'))

    director = relationship("Director")