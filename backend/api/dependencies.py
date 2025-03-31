from fastapi import Depends

from application.services.visualization_service import VisualizationService
from core.config import Settings
from domain.ports.visualization import IVisualizationRepository, IVisualizationService
from infrastructure.repositories.visualization_repository import (
    JSONVisualizationRepository,
)


def get_settings() -> Settings:
    return Settings()


def get_visualization_repository(
    settings: Settings = Depends(get_settings),
) -> IVisualizationRepository:
    return JSONVisualizationRepository(settings.DATA_FILE_PATH)


def get_visualization_service(
    repo: IVisualizationRepository = Depends(get_visualization_repository),
) -> IVisualizationService:
    return VisualizationService(repo)
