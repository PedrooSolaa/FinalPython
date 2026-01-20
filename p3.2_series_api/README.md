# API de Series de Televisión con SQLAlchemy

**Autor:** Pedro Sola

## Descripción

API REST desarrollada con FastAPI para la gestión de series de televisión, utilizando SQLAlchemy para persistencia en base de datos SQLite. Permite realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sobre una base de datos persistente.

## Dominio de Datos

El dominio elegido son **series de televisión** porque:

- Es un tema fácil de entender para cualquier usuario
- Permite modelar diferentes tipos de datos
- Ofrece opciones interesantes para practicar validaciones (puntuaciones entre 0-10, número de temporadas, etc.)
- Es un caso de uso real que podría tener aplicaciones prácticas.

### Modelo de Datos

Cada serie contiene:
- **id**: Identificador único (autogenerado)
- **titulo**: Nombre de la serie
- **generos**: Lista de géneros
- **puntuacion**: Valoración de 0.0 a 10.0
- **finalizada**: Si la serie ha terminado o sigue emitiéndose
- **fecha_estreno**: Fecha de estreno en formato YYYY-MM-DD
- **temporadas**: Número de temporadas

## Pruebas

El archivo `test_endpoints/series.rest` contiene ejemplos de peticiones para probar todos los endpoints. Necesitas la extensión **REST Client** de VS Code para ejecutarlas.