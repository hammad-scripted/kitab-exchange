from fastapi import Request, status
from fastapi.responses import JSONResponse


class NotFoundException(Exception):
    def __init__(self, message: str, status_code=status.HTTP_404_NOT_FOUND):
        self.message = message
        self.status_code = status_code


class BadRequestException(Exception):
    def __init__(self, message: str, status_code=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code


class InternalServerException(Exception):
    def __init__(self, message: str, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code


# Custom exception handlers returning dynamic error messages
async def bad_request_exception_handler(request: Request, exc: BadRequestException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "Bad Request", "message": exc.message},
    )


async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "Not Found", "message": exc.message},
    )


async def internal_server_exception_handler(request: Request, exc: InternalServerException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "Internal Server Error", "message": exc.message},
    )