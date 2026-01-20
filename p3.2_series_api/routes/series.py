from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from database.database import SessionLocal
from models.serie import Serie
from schemas.serie import SerieCreate, SerieResponse

router = APIRouter(
    prefix="/series",
    tags=["series"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def serie_to_response(serie: Serie) -> SerieResponse:
    return SerieResponse(
        id=serie.id,
        titulo=serie.titulo,
        generos=serie.generos.split(',') if serie.generos else [],
        puntuacion=serie.puntuacion,
        finalizada=serie.finalizada,
        fecha_estreno=serie.fecha_estreno,
        temporadas=serie.temporadas,
        director_id=serie.director_id,
        director=serie.director
    )

@router.get("/", response_model=List[SerieResponse])
def get_series(db: Session = Depends(get_db)):
    series = db.query(Serie).options(joinedload(Serie.director)).all()
    return [serie_to_response(s) for s in series]

@router.get("/{serie_id}", response_model=SerieResponse)
def get_serie(serie_id: int, db: Session = Depends(get_db)):
    serie = db.query(Serie).options(joinedload(Serie.director)).filter(Serie.id == serie_id).first()
    if not serie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Serie no encontrada"
        )
    return serie_to_response(serie)

@router.post("/", response_model=SerieResponse, status_code=status.HTTP_201_CREATED)
def create_serie(serie: SerieCreate, db: Session = Depends(get_db)):
    # Check if serie with same titulo exists, or perhaps allow duplicates
    # For now, allow duplicates

    new_serie = Serie(
        titulo=serie.titulo,
        generos=','.join(serie.generos),
        puntuacion=serie.puntuacion,
        finalizada=serie.finalizada,
        fecha_estreno=serie.fecha_estreno,
        temporadas=serie.temporadas
    )
    db.add(new_serie)
    db.commit()
    db.refresh(new_serie)
    return serie_to_response(new_serie)

@router.put("/{serie_id}", response_model=SerieResponse)
def update_serie(serie_id: int, serie: SerieCreate, db: Session = Depends(get_db)):
    stored_serie = db.query(Serie).filter(Serie.id == serie_id).first()
    if not stored_serie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Serie no encontrada"
        )

    stored_serie.titulo = serie.titulo
    stored_serie.generos = ','.join(serie.generos)
    stored_serie.puntuacion = serie.puntuacion
    stored_serie.finalizada = serie.finalizada
    stored_serie.fecha_estreno = serie.fecha_estreno
    stored_serie.temporadas = serie.temporadas

    db.commit()
    db.refresh(stored_serie)
    return serie_to_response(stored_serie)

@router.delete("/{serie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_serie(serie_id: int, db: Session = Depends(get_db)):
    serie = db.query(Serie).filter(Serie.id == serie_id).first()
    if not serie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Serie no encontrada"
        )

    db.delete(serie)
    db.commit()