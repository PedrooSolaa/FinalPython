from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker

from database.database import Base, engine, SessionLocal
from routes import series, directors
from models.serie import Serie
from models.director import Director

Base.metadata.create_all(bind=engine)

# Seed initial data
def seed_data():
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Serie).count() == 0:
            # Create directors first
            directors_data = [
                Director(name="Vince", surname="Gilligan"),
                Director(name="Matt", surname="Duffer"),
                Director(name="Greg", surname="Daniels")
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

seed_data()

app = FastAPI()

app.include_router(series.router)
app.include_router(directors.router)

@app.get("/")
def root():
    return {"message": "API de Series de Televisión con FastAPI y SQLite"}