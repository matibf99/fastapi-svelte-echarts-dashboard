from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.dependencies import get_settings
from api.routers import health_router, visualization_router
from core.config import Settings


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title=settings.API_TITLE, version=settings.API_VERSION, root_path="/api"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(visualization_router.router)
    app.include_router(health_router.router)

    app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="static")

    return app


settings: Settings = get_settings()
app = create_app(settings)
