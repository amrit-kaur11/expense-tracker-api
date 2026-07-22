from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.logging import logger


class AppException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class EntityNotFoundException(AppException):
    def __init__(self, message: str = "Requested resource not found"):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)


class EntityAlreadyExistsException(AppException):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message=message, status_code=status.HTTP_409_CONFLICT)


class AuthenticationException(AppException):
    def __init__(self, message: str = "Could not validate credentials"):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED)


class PermissionDeniedException(AppException):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN)


class ValidationException(AppException):
    def __init__(self, message: str = "Invalid input data"):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)


class StorageException(AppException):
    def __init__(self, message: str = "Storage operation failed"):
        super().__init__(message=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    logger.warning(f"AppException raised on {request.method} {request.url.path}: status={exc.status_code}, detail={exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
