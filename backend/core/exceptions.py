from fastapi import HTTPException, status


class DataValidationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )


class DataNotFoundError(HTTPException):
    def __init__(self, detail: str = "Requested data not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class DataProviderError(HTTPException):
    def __init__(self, detail: str = "Error accessing data source"):
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)
