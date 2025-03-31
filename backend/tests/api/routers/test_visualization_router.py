from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from api.dependencies import get_visualization_service
from core.exceptions import DataNotFoundError, DataValidationError
from domain.models.visualization import BarPlotData, PieChartData, VisualizationData
from domain.ports.visualization import IVisualizationService
from main import app as fastapi_app


@pytest.fixture
def mock_visualization_service():
    """Crea un mock para IVisualizationService."""
    return AsyncMock(spec=IVisualizationService)


@pytest.fixture
def sample_visualization_data() -> VisualizationData:
    """Datos de ejemplo para devolver por el mock."""
    return VisualizationData(
        piechart=PieChartData(labels=["P1", "P2"], values=[30, 70]),
        barplot=BarPlotData(categories=["M1", "M2"], values=[120, 180]),
    )


@pytest.fixture(autouse=True)
def override_dependency(mock_visualization_service: AsyncMock):
    """Sobrescribe la dependencia del servicio para todos los tests en este archivo."""
    original_override = fastapi_app.dependency_overrides.get(get_visualization_service)
    fastapi_app.dependency_overrides[get_visualization_service] = (
        lambda: mock_visualization_service
    )
    yield
    # Restaura el estado original o limpia
    if original_override:
        fastapi_app.dependency_overrides[get_visualization_service] = original_override
    elif get_visualization_service in fastapi_app.dependency_overrides:
        del fastapi_app.dependency_overrides[get_visualization_service]


# --- Tests ---


@pytest.mark.asyncio
async def test_get_data_success(
    mock_visualization_service: AsyncMock, sample_visualization_data: VisualizationData
):
    """Testea el endpoint /api/data con respuesta exitosa."""
    mock_visualization_service.get_visualization_data.return_value = (
        sample_visualization_data
    )

    client = TestClient(fastapi_app)
    response = client.get("/api/data")

    assert response.status_code == 200
    response_data = response.json()
    assert (
        response_data["piechart"]["labels"] == sample_visualization_data.piechart.labels
    )
    assert (
        response_data["barplot"]["values"] == sample_visualization_data.barplot.values
    )
    mock_visualization_service.get_visualization_data.assert_called_once()


@pytest.mark.asyncio
async def test_get_data_not_found(mock_visualization_service: AsyncMock):
    """Testea el endpoint /api/data cuando los datos no se encuentran (404)."""
    error_message = "Data file could not be located."
    mock_visualization_service.get_visualization_data.side_effect = DataNotFoundError(
        error_message
    )

    client = TestClient(fastapi_app)
    response = client.get("/api/data")

    assert response.status_code == 404
    assert response.json() == {"detail": error_message}
    mock_visualization_service.get_visualization_data.assert_called_once()


@pytest.mark.asyncio
async def test_get_data_validation_error(mock_visualization_service: AsyncMock):
    """Testea el endpoint /api/data cuando hay un error de validación (422)."""
    error_message = "Invalid data structure in file."
    mock_visualization_service.get_visualization_data.side_effect = DataValidationError(
        error_message
    )

    client = TestClient(fastapi_app)
    response = client.get("/api/data")

    assert response.status_code == 422
    assert response.json() == {"detail": error_message}
    mock_visualization_service.get_visualization_data.assert_called_once()


@pytest.mark.asyncio
async def test_get_data_generic_error(mock_visualization_service: AsyncMock):
    """Testea el endpoint /api/data con un error genérico del servidor (500)."""
    mock_visualization_service.get_visualization_data.side_effect = Exception(
        "Generic internal error"
    )

    client = TestClient(fastapi_app)
    response = client.get("/api/data")

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error."}
    mock_visualization_service.get_visualization_data.assert_called_once()
