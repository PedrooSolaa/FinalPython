from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.database import SessionLocal
from models.director import Director
from schemas.director import DirectorCreate, DirectorResponse

router = APIRouter(
    prefix="/directors",
    tags=["directors"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[DirectorResponse])
def get_directors(db: Session = Depends(get_db)):
    return db.query(Director).all()

@router.get("/{director_id}", response_model=DirectorResponse)
def get_director(director_id: int, db: Session = Depends(get_db)):
    director = db.query(Director).filter(Director.id == director_id).first()
    if not director:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Director no encontrado"
        )
    return director

@router.post("/", response_model=DirectorResponse, status_code=status.HTTP_201_CREATED)
def create_director(director: DirectorCreate, db: Session = Depends(get_db)):
    new_director = Director(**director.dict())
    db.add(new_director)
    db.commit()
    db.refresh(new_director)
    return new_director

@router.put("/{director_id}", response_model=DirectorResponse)
def update_director(director_id: int, director: DirectorCreate, db: Session = Depends(get_db)):
    stored_director = db.query(Director).filter(Director.id == director_id).first()
    if not stored_director:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Director no encontrado"
        )

    for key, value in director.dict().items():
        setattr(stored_director, key, value)

    db.commit()
    db.refresh(stored_director)
    return stored_director

@router.delete("/{director_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_director(director_id: int, db: Session = Depends(get_db)):
    director = db.query(Director).filter(Director.id == director_id).first()
    if not director:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Director no encontrado"
        )

    db.delete(director)
    db.commit()