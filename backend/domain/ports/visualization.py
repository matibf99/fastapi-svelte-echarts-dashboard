from abc import ABC, abstractmethod

from domain.models.visualization import VisualizationData


class IVisualizationRepository(ABC):
    @abstractmethod
    async def get_data(self) -> VisualizationData:
        pass


class IVisualizationService(ABC):
    @abstractmethod
    async def get_visualization_data(self) -> VisualizationData:
        pass
