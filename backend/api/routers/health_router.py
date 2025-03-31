from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(tags=["health"], responses={404: {"description": "Not found"}})


@router.get(
    "/health",
)
async def health_check() -> JSONResponse:
    return JSONResponse(content={"status": "OK"})
