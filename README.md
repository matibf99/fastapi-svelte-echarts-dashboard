# Visualización de datos con FastAPI, Svelte y eCharts

Aplicación full-stack que consume datos desde un archivo JSON, los sirve a través de una API REST construida con FastAPI y los visualiza en un dashboard utilizando SvelteKit y ECharts. El proyecto está completamente dockerizado para facilitar su despliegue y ejecución.

## ✨ Características principales

*   **Backend:** API REST implementada con FastAPI siguiendo principios de **arquitectura limpia** y **SOLID** para mantenibilidad y escalabilidad.
*   **Frontend:** Interfaz de usuario reactiva construida con **SvelteKit 5** y **TypeScript**.
*   **Visualizaciones interactivas:** Gráficos (circular y barras) renderizados con **ECharts**.
*   **Estilado eficiente:** Interfaz estilada con **Tailwind CSS 4**.
*   **Dockerizado:** Configuración completa con `Dockerfile` (multi-etapa) y `docker-compose.yml` para un despliegue sencillo.
*   **Gestión de dependencias:** **Poetry** para el backend y **npm** para el frontend.
*   **Testing:** Tests unitarios y de integración para backend (`pytest`) y frontend (`vitest`).

## 🚀 Tecnologías utilizadas

*   **Backend:**
    *   Python 3.12+
    *   FastAPI
    *   Pydantic (Validación de datos y configuración)
    *   Uvicorn (Servidor ASGI)
    *   Poetry (Gestión de dependencias y entorno)
    *   pytest, pytest-asyncio (Testing)
*   **Frontend:**
    *   SvelteKit 5
    *   TypeScript
    *   ECharts (Librería de gráficos)
    *   Tailwind CSS 4 (Framework CSS)
    *   Vite (Build tool)
    *   Vitest (Testing)
*   **Infraestructura & DevOps:**
    *   Docker
    *   Docker Compose

## 📂 Estructura del proyecto

```
/prueba-tecnica-rd
├── backend/               # Código fuente del servidor API (FastAPI)
│   ├── api/               # Capa de presentación (routers, dependencias)
│   ├── application/       # Lógica de negocio (servicios)
│   ├── core/              # Configuración, excepciones base
│   ├── domain/            # Modelos de dominio y puertos (interfaces)
│   ├── infrastructure/    # Implementaciones concretas (repositorios)
│   ├── tests/             # Tests unitarios y de integración del backend
│   ├── main.py            # Punto de entrada de la aplicación backend
│   ├── pyproject.toml     # Definición del proyecto y dependencias (Poetry)
│   ├── poetry.lock        # Archivo de bloqueo de dependencias (Poetry)
│   └── requirements.txt   # Exportado desde Poetry (SOLO producción, para Docker)
├── frontend/              # Código fuente de la interfaz (SvelteKit)
│   ├── src/
│   │   ├── lib/           # Componentes, API utils, servicios, tipos
│   │   └── routes/        # Definición de páginas/vistas
│   ├── static/            # Archivos estáticos (favicon, etc.)
│   ├── package.json       # Dependencias y scripts del frontend
│   ├── svelte.config.js   # Configuración de SvelteKit
│   └── vite.config.ts     # Configuración de Vite
├── data.json              # Archivo con los datos para los gráficos
├── Dockerfile             # Instrucciones para construir la imagen Docker de la app
├── docker-compose.yml     # Orquestación del servicio con Docker Compose
├── .gitignore             # Archivos y carpetas a ignorar por Git
└── README.md              # Este archivo
```

## ⚙️ Prerrequisitos

*   Git
*   Docker
*   Docker Compose
*   Node.js (v18 o superior para el desarrollo frontend)
*   Python (v3.12 o superior para el desarrollo backend)
*   Poetry (Gestor de paquetes Python: `pip install poetry`)

## 🛠️ Instalación y configuración local

1.  **Clonar el repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd prueba-tecnica-rd
    ```

2.  **Crear archivo `data.json`:**
    Crea un archivo llamado `data.json` en la raíz del proyecto con el siguiente contenido de ejemplo (o con tus propios datos):
    ```json
    {
      "piechart": {
        "labels": ["Producto A", "Producto B", "Producto C", "Producto D"],
        "values": [25, 30, 20, 25]
      },
      "barplot": {
        "categories": ["Enero", "Febrero", "Marzo", "Abril"],
        "values": [150, 200, 180, 220]
      }
    }
    ```

3.  **Crear archivo `.env` (Opcional - para desarrollo local):**
    Crea un archivo `.env` en la raíz del proyecto. Docker Compose usará las variables definidas en `docker-compose.yml`, pero este archivo es útil para desarrollo local fuera de Docker.
    ```ini
    # Backend
    API_TITLE="Data Visualization API Dev"
    API_VERSION="1.0.0-dev"
    DATA_FILE_PATH="./data.json" # Ruta relativa para dev local

    # Frontend
    VITE_API_URL="http://localhost:8000/api"
    ```

## 💻 Desarrollo local

Puedes ejecutar el backend y el frontend por separado para desarrollo.

### Backend (FastAPI)

```bash
# 1. Navega a la carpeta backend
cd backend

# 2. Instala dependencias (producción y desarrollo)
poetry install

# 3. Ejecuta el servidor con recarga automática
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
El backend estará disponible en `http://localhost:8000`.

### Frontend (SvelteKit)

```bash
# 1. Navega a la carpeta frontend
cd frontend

# 2. Instala dependencias
npm install

# 3. Inicia el servidor de desarrollo
npm run dev -- --open
```
El frontend estará disponible en `http://localhost:5173` (o el puerto que Vite indique).

## ✅ Testing

### Backend

```bash
# 1. Navega a la carpeta backend
cd backend

# 2. Ejecuta los tests con pytest (asegúrate de haber corrido 'poetry install' antes)
poetry run pytest
```

### Frontend

```bash
# 1. Navega a la carpeta frontend
cd frontend

# 2. Ejecuta los tests con Vitest (asegúrate de haber corrido 'npm install' antes)
npm run test
```

## 🐳 Despliegue con Docker

La forma más sencilla de ejecutar la aplicación completa es usando Docker Compose.

### Nota sobre requirements.txt

El archivo backend/requirements.txt utilizado por el Dockerfile debe contener únicamente las dependencias de producción. Si estás desarrollando con Poetry, asegúrate de generar este archivo correctamente antes de construir la imagen Docker (o asegúrate de que la versión correcta esté commiteada).

```bash
# Navega a la carpeta backend
cd backend

# Genera el requirements.txt solo con dependencias de producción
poetry export --only main --without-hashes --format=requirements.txt > requirements.txt

# Vuelve a la raíz si es necesario
cd ..
```    

### Comandos de Docker Compose

1.  **Construir la imagen Docker:**
    (Este paso es opcional si solo quieres ejecutar, `docker-compose up` lo hará si la imagen no existe)
    ```bash
    docker-compose build
    ```

2.  **Iniciar la aplicación:**
    ```bash
    docker-compose up -d
    ```
    La aplicación completa (frontend sirviendo los datos del backend) estará disponible en: `http://localhost:8000`

3.  **Detener la aplicación:**
    ```bash
    docker-compose down
    ```

## 📡 Endpoints de la API

El backend expone los siguientes endpoints bajo el prefijo `/api`:

*   `GET /api/data`: Obtiene los datos combinados para el gráfico circular y el gráfico de barras desde `data.json`.
*   `GET /api/health`: Endpoint simple para verificar que el servicio backend está en funcionamiento. Devuelve `{"status": "OK"}`.

El frontend se sirve desde la raíz (`/`).

## 🏛️ Notas de la arquitectura del Backend

El backend sigue los principios de la Arquitectura Limpia, separando las responsabilidades en capas:

*   **Dominio:** Contiene los modelos de datos (`models`) y las abstracciones (`ports`). No depende de ninguna otra capa.
*   **Aplicación:** Contiene la lógica de negocio (`services`). Depende de las abstracciones del dominio.
*   **Infraestructura:** Contiene las implementaciones concretas de las abstracciones (`repositories`). Depende del dominio.
*   **API/Presentación:** Contiene los routers de FastAPI y la inyección de dependencias. Orquesta el flujo y depende de la capa de aplicación.

Esto promueve un código desacoplado, más fácil de testear y mantener.
