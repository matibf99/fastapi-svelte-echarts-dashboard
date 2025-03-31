from domain.models.visualization import VisualizationData
from domain.ports.visualization import IVisualizationRepository, IVisualizationService


class VisualizationService(IVisualizationService):
    def __init__(self, repository: IVisualizationRepository):
        self._repo = repository

    async def get_visualization_data(self) -> VisualizationData:
        try:
            return await self._repo.get_data()
        except Exception as e:
            raise e
