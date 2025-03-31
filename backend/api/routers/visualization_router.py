from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_visualization_service
from core.exceptions import DataNotFoundError, DataValidationError
from domain.models.visualization import VisualizationData
from domain.ports.visualization import IVisualizationService

router = APIRouter(
    tags=["visualization_data"], responses={404: {"description": "Not found"}}
)


@router.get(
    "/data",
    summary="Get visualization data",
    description="Retrieves data for piechart and barplot visualization",
    response_description="JSON with visualization data",
)
async def get_data(
    data_service: IVisualizationService = Depends(get_visualization_service),
) -> VisualizationData:
    try:
        data = await data_service.get_visualization_data()
        return data
    except DataNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e.detail))
    except DataValidationError as e:
        raise HTTPException(status_code=422, detail=str(e.detail))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")
