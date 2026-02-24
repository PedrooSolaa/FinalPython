# API de Series de Televisión

API REST desarrollada con FastAPI y SQLAlchemy para gestionar series de televisión y sus directores.

## 🚀 Características

- **CRUD completo** para Series y Directores
- **Base de datos** SQLite (desarrollo) / PostgreSQL (producción)
- **Documentación automática** con Swagger/OpenAPI
- **CORS** habilitado
- **Docker** ready
- **Despliegue** en Render

## 📋 Requisitos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)


### 1. Acceder a la aplicación

- **API**: http://localhost:8080
- **Documentación Swagger**: http://localhost:8080/docs
- **Documentación ReDoc**: http://localhost:8080/redoc

## 📁 Estructura del Proyecto

```
FinalPython/
├── app.py                      # Punto de entrada principal
├── Dockerfile                  # Configuración Docker
├── docker-compose.yml          # Docker Compose
├── Procfile                    # Configuración para Render
├── requirements.txt            # Dependencias Python
├── README.md                   # Este archivo
└── p3.2_series_api/
    ├── main.py                 # Aplicación FastAPI
    ├── database/
    │   ├── __init__.py
    │   └── database.py         # Configuración SQLAlchemy
    ├── models/
    │   ├── __init__.py
    │   ├── director.py         # Modelo Director
    │   └── serie.py            # Modelo Serie
    ├── routes/
    │   ├── __init__.py
    │   ├── directors.py        # Endpoints de directores
    │   └── series.py           # Endpoints de series
    ├── schemas/
    │   ├── __init__.py
    │   ├── director.py         # Schemas Pydantic Director
    │   └── serie.py            # Schemas Pydantic Serie
    └── test_endpoints/
        ├── directors.rest      # Tests directores
        └── series.rest         # Tests series
```

## 🌐 API Endpoints

### Series

- `GET /series` - Listar todas las series
- `GET /series/{id}` - Obtener una serie por ID
- `POST /series` - Crear una nueva serie
- `PUT /series/{id}` - Actualizar una serie
- `DELETE /series/{id}` - Eliminar una serie
- `GET /series/search/{nombre}` - Buscar series por nombre

### Directores

- `GET /directors` - Listar todos los directores
- `GET /directors/{id}` - Obtener un director por ID
- `POST /directors` - Crear un nuevo director
- `PUT /directors/{id}` - Actualizar un director
- `DELETE /directors/{id}` - Eliminar un director

## 🐳 Despliegue con Docker

### Usando Docker

```bash
docker build -t series-api .
docker run -p 8000:8000 series-api
```

### Usando Docker Compose

```bash
docker-compose up
```

## ☁️ Despliegue en Render

### Paso 1: Preparar el repositorio

Asegúrate de tener estos archivos en tu repositorio:
- `app.py`
- `Dockerfile`
- `Procfile`
- `requirements.txt`

### Paso 2: Crear Web Service en Render

1. Ve a [Render Dashboard](https://dashboard.render.com)
2. Click en **"New +"** → **"Web Service"**
3. Conecta tu repositorio de GitHub/GitLab
4. Configura el servicio:
   - **Name**: `series-api` (o el nombre que prefieras)
   - **Environment**: `Docker`
   - **Region**: Selecciona la más cercana
   - **Branch**: `main` (o tu rama principal)

### Paso 3: Configuración

Render detectará automáticamente el `Dockerfile` y el `Procfile`.

**Si usas Docker:**
- **Docker Command**: Se usa automáticamente del Dockerfile
- No necesitas configurar Start Command

**Variables de entorno (opcional):**
- `DATABASE_URL`

### Paso 4: Deploy

1. Click en **"Create Web Service"**
2. Render comenzará el build y deploy automáticamente
3. Una vez completado, verás la URL de tu API

### Paso 5: Verificar

Accede a:
- `https://tu-servicio.onrender.com/` - Mensaje de bienvenida
- `https://tu-servicio.onrender.com/docs` - Documentación Swagger

### Producción (PostgreSQL)

Para usar PostgreSQL en Render:

1. En Render, ve a **"New +"** → **"PostgreSQL"**
2. Crea la base de datos
3. En tu Web Service, ve a **"Environment"**
4. La variable `DATABASE_URL` se añade automáticamente si vinculas la BD

El código maneja automáticamente la conversión de `postgres://` a `postgresql://`

## 📝 Datos de Ejemplo

Al iniciar, la aplicación carga automáticamente datos de ejemplo:

**Series:**
- Breaking Bad
- The Sopranos
- The Wire
- Stranger Things

**Directores:**
- Vince Gilligan
- David Chase
- David Simon
- The Duffer Brothers

