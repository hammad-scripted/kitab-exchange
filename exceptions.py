from fastapi import status
from fastapi.responses import JSONResponse
from fastapi import Request


class NotFoundException(Exception):
    def __init__(self, message, status_code=status.HTTP_404_NOT_FOUND):
        self.message = message
        self.status_code = status_code


class BadRequestException(Exception):
    def __init__(self, message, status_code=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code


class InternalServerException(Exception):
    def __init__(self, message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code


# custom exception handlers


async def bad_request_exception_handler(request: Request, exc):
    return JSONResponse(status_code=400, content={"message": "Bad Request"})


async def not_found_exception_handler(request: Request, exc):
    return JSONResponse(status_code=404, content={"message": "Not Found"})


async def internal_server_exception_handler(request: Request, exc):
    return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
