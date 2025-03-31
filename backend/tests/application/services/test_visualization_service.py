from unittest.mock import AsyncMock

import pytest

from application.services.visualization_service import VisualizationService
from core.exceptions import DataNotFoundError
from domain.models.visualization import BarPlotData, PieChartData, VisualizationData
from domain.ports.visualization import IVisualizationRepository


@pytest.fixture
def mock_repo():
    """Crea un mock para IVisualizationRepository."""
    return AsyncMock(spec=IVisualizationRepository)


@pytest.fixture
def visualization_service(mock_repo: AsyncMock) -> VisualizationService:
    """Crea una instancia del servicio con el repositorio mockeado."""
    return VisualizationService(repository=mock_repo)


@pytest.fixture
def sample_visualization_data() -> VisualizationData:
    """Datos de ejemplo para devolver por el mock."""
    return VisualizationData(
        piechart=PieChartData(labels=["A", "B"], values=[10, 90]),
        barplot=BarPlotData(categories=["X", "Y"], values=[50, 150]),
    )


# --- Tests ---


@pytest.mark.asyncio
async def test_get_visualization_data_success(
    visualization_service: VisualizationService,
    mock_repo: AsyncMock,
    sample_visualization_data: VisualizationData,
):
    """Verifica que el servicio llama al repo y devuelve los datos."""
    mock_repo.get_data.return_value = sample_visualization_data

    result = await visualization_service.get_visualization_data()

    mock_repo.get_data.assert_called_once()
    assert result == sample_visualization_data
    assert isinstance(result, VisualizationData)


@pytest.mark.asyncio
async def test_get_visualization_data_repo_raises_exception(
    visualization_service: VisualizationService, mock_repo: AsyncMock
):
    """Verifica que el servicio propaga las excepciones del repositorio."""
    mock_repo.get_data.side_effect = DataNotFoundError("Test error")

    with pytest.raises(DataNotFoundError) as excinfo:
        await visualization_service.get_visualization_data()

    assert "Test error" in str(excinfo.value)
    mock_repo.get_data.assert_called_once()
