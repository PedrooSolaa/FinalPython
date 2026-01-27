from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time

from database.database import Base, engine
from routes import series, directors

# Create database tables
Base.metadata.create_all(bind=engine)

# Seed initial data
series.seed_data()

# Create FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware for logging request time
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(f"{request.method} {request.url.path} - {process_time:.4f}s")
    return response

# Include routers
app.include_router(series.router)
app.include_router(directors.router)

@app.get("/")
def root():
    return {"message": "API de Series de Televisión con FastAPI y SQLite"}