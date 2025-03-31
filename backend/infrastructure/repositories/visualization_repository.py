import json
from pathlib import Path

from core.exceptions import DataNotFoundError, DataValidationError
from domain.models.visualization import VisualizationData
from domain.ports.visualization import IVisualizationRepository


class JSONVisualizationRepository(IVisualizationRepository):
    def __init__(self, file_path: Path):
        self._file_path = file_path

    async def get_data(self) -> VisualizationData:
        try:
            with open(self._file_path, "r", encoding="utf-8") as file:
                raw_data = json.load(file)
                return VisualizationData.from_json(raw_data)
        except FileNotFoundError:
            raise DataNotFoundError(f"Data file not found at {self._file_path}")
        except json.JSONDecodeError:
            raise DataValidationError("Invalid JSON format in data file")
        except ValueError as e:
            raise DataValidationError(f"Data validation failed: {str(e)}")
