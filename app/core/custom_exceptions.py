class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400, errors=None):
        self.message = message
        self.status_code = status_code
        self.errors = errors or []
        super().__init__(message)


class FileTypeNotAllowed(AppException):
    def __init__(self):
        super().__init__(
            message="Only CSV files are allowed",
            status_code=415
        )


class FileTooLargeError(AppException):
    def __init__(self):
        super().__init__(
            message="Uploaded file exceeds allowed size",
            status_code=413
        )


class CSVValidationException(AppException):
    def __init__(self, errors):
        super().__init__(
            message="CSV validation failed",
            status_code=422,
            errors=errors
        )
