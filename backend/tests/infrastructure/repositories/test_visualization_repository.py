import json
from pathlib import Path

import pytest

from core.exceptions import DataNotFoundError, DataValidationError
from domain.models.visualization import VisualizationData
from infrastructure.repositories.visualization_repository import (
    JSONVisualizationRepository,
)

# Datos de ejemplo para los tests
VALID_DATA = {
    "piechart": {"labels": ["Producto A", "Producto B"], "values": [10, 20]},
    "barplot": {"categories": ["Enero", "Febrero"], "values": [100, 200]},
}
INVALID_JSON_CONTENT = '{"piechart": {"labels": ["Producto A", "Producto B"], "values": [10, 20]}, "barplot": missing_bracket'


@pytest.fixture
def valid_data_file(tmp_path: Path) -> Path:
    """Crea un archivo data.json temporal válido."""
    file_path = tmp_path / "data.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(VALID_DATA, f)
    return file_path


@pytest.fixture
def invalid_json_file(tmp_path: Path) -> Path:
    """Crea un archivo data.json temporal con JSON inválido."""
    file_path = tmp_path / "invalid_data.json"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(INVALID_JSON_CONTENT)
    return file_path


@pytest.fixture
def non_existent_file(tmp_path: Path) -> Path:
    """Devuelve una ruta a un archivo que no existe."""
    return tmp_path / "non_existent_data.json"


# --- Tests ---


@pytest.mark.asyncio
async def test_get_data_success(valid_data_file: Path):
    """Verifica la lectura exitosa de datos válidos."""
    repo = JSONVisualizationRepository(valid_data_file)
    data = await repo.get_data()
    assert isinstance(data, VisualizationData)
    assert data.piechart.labels == VALID_DATA["piechart"]["labels"]
    assert data.barplot.values == VALID_DATA["barplot"]["values"]


@pytest.mark.asyncio
async def test_get_data_file_not_found(non_existent_file: Path):
    """Verifica que se lanza DataNotFoundError si el archivo no existe."""
    repo = JSONVisualizationRepository(non_existent_file)
    with pytest.raises(DataNotFoundError):
        await repo.get_data()


@pytest.mark.asyncio
async def test_get_data_invalid_json(invalid_json_file: Path):
    """Verifica que se lanza DataValidationError si el JSON es inválido."""
    repo = JSONVisualizationRepository(invalid_json_file)
    with pytest.raises(DataValidationError) as excinfo:
        await repo.get_data()
    assert "Invalid JSON format" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_data_validation_error(tmp_path: Path):
    """Verifica que se lanza DataValidationError si los datos no cumplen el modelo."""
    invalid_structure_data = {
        "piechart": {"labels": ["Producto A"], "values": [10, 20]},  # Mismatch 2 vs 1
        "barplot": {"categories": ["Enero"], "values": [100]},
    }
    file_path = tmp_path / "invalid_structure.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(invalid_structure_data, f)

    repo = JSONVisualizationRepository(file_path)
    with pytest.raises(DataValidationError) as excinfo:
        await repo.get_data()
    assert "validation failed" in str(excinfo.value).lower()
