"""Custom HTTP exceptions."""

from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Thông tin đăng nhập không hợp lệ",
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Bạn không có quyền thực hiện thao tác này"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class NotFoundException(HTTPException):
    def __init__(self, entity: str = "Tài nguyên"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity} không tồn tại",
        )


class BadRequestException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class InvalidTransitionException(BadRequestException):
    def __init__(self, current_status: str, action: str):
        super().__init__(
            detail=f"Không thể thực hiện '{action}' khi trạng thái là '{current_status}'"
        )
