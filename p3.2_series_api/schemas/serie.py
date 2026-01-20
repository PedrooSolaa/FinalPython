from pydantic import BaseModel
from typing import List
from schemas.director import DirectorResponse

class SerieBase(BaseModel):
    titulo: str
    generos: List[str]
    puntuacion: float
    finalizada: bool
    fecha_estreno: str
    temporadas: int
    director_id: int

class SerieCreate(SerieBase):
    pass

class SerieResponse(SerieBase):
    id: int
    director: DirectorResponse

    class Config:
        from_attributes = True