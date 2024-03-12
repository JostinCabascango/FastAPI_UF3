# Ecommerce FastAPI

Este proyecto es una API de comercio electrónico construida con FastAPI. Proporciona una serie de endpoints para
gestionar productos, categorías y subcategorías. Además, permite la inserción masiva de productos a través de archivos
CSV.

## Requisitos

Este proyecto requiere Python 3.8 o superior. Todas las dependencias necesarias están especificadas en el
archivo `requirements.txt`. Para instalar estas dependencias, ejecuta el siguiente comando en tu terminal:

```bash
pip install -r requirements.txt
```

## Ejecución

Para ejecutar este proyecto, utiliza el siguiente comando:

```bash
uvicorn main:app --reload
```

Esto iniciará el servidor en `http://127.0.0.1:8000`.

## Documentación

La documentación de la API se genera automáticamente y se puede acceder a ella en `http://127.0.0.1:8000/docs` cuando el
servidor está en ejecución.

## Características

Este proyecto incluye las siguientes características:

- **Productos**: Permite crear, leer, actualizar y eliminar productos.
- **Categorías**: Permite crear, leer, actualizar y eliminar categorías.
- **Subcategorías**: Permite crear, leer, actualizar y eliminar subcategorías.
- **Carga masiva de productos**: Permite la inserción masiva de productos a través de archivos CSV.

## Demo

Puedes ver una demostración de cómo funcionan todos los endpoints en el siguiente video:

[Ver Demo](https://drive.google.com/file/d/1BCYs31Y6SNdHEsFsGZ7GIKKZqkpXZx-R/view?usp=drive_link)