from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from database.database import SessionLocal
from models.serie import Serie
from models.director import Director
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

def seed_data():
    """Initialize database with sample data"""
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Serie).count() == 0:
            # Create directors first
            directors_data = [
                Director(name="Vince", surname="Gilligan", edad=57, lugar_nacimiento="Richmond, Virginia"),
                Director(name="Matt", surname="Duffer", edad=40, lugar_nacimiento="Durham, North Carolina"),
                Director(name="Greg", surname="Daniels", edad=61, lugar_nacimiento="New York City, New York")
            ]
            db.add_all(directors_data)
            db.commit()
            db.refresh(directors_data[0])
            db.refresh(directors_data[1])
            db.refresh(directors_data[2])

            series_data = [
                Serie(
                    titulo="Breaking Bad",
                    generos="Drama,Crimen,Thriller",
                    puntuacion=9.5,
                    finalizada=True,
                    fecha_estreno="2008-01-20",
                    temporadas=5,
                    director_id=directors_data[0].id
                ),
                Serie(
                    titulo="Stranger Things",
                    generos="Ciencia Ficción,Terror,Drama",
                    puntuacion=8.7,
                    finalizada=False,
                    fecha_estreno="2016-07-15",
                    temporadas=4,
                    director_id=directors_data[1].id
                ),
                Serie(
                    titulo="The Office",
                    generos="Comedia,Mockumentary",
                    puntuacion=9.0,
                    finalizada=True,
                    fecha_estreno="2005-03-24",
                    temporadas=9,
                    director_id=directors_data[2].id
                )
            ]
            db.add_all(series_data)
            db.commit()
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
        temporadas=serie.temporadas,
        director_id=serie.director_id
    )
    db.add(new_serie)
    db.commit()
    db.refresh(new_serie)
    # Reload with director relationship
    new_serie = db.query(Serie).options(joinedload(Serie.director)).filter(Serie.id == new_serie.id).first()
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