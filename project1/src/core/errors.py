class AppError(Exception):
    """Base class for user-facing application errors."""


class ValidationError(AppError):
    """Raised when the input JSON does not match the expected schema."""


class SampleNotFoundError(AppError):
    """Raised when a sample cannot be found or is ambiguous."""


class NotImplementedFeatureError(AppError):
    """Raised for reserved commands that are not implemented yet."""