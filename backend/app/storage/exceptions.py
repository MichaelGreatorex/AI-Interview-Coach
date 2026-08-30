class InvalidDocumentUploadError(ValueError):
    """Raised when an uploaded document fails validation."""


class FileTooLargeError(Exception):
    """Raised when an uploaded file exceeds the configured size limit."""