"""Custom exceptions raised during configuration parsing."""


class ParsingError(Exception):
    """Base exception for parsing errors."""

    def __init__(self):
        """Initialize the parsing error with a standard message."""
        msg = '[Parsing Error]: Invalid input'
        super().__init__(msg)


class DroneNumberError(ParsingError):
    """Raised when the drone number line is malformed."""

    def __init__(self):
        """Initialize the drone number error with a standard message."""
        msg = '[Parsing Error]: Invalid drone number'
        super().__init__(msg)


class FormatError(ParsingError):
    """Raised when input format is invalid."""

    def __init__(self):
        """Fromat error in config maze files."""
        msg = '[Parsing Error]: Invalid format'
        super().__init__(msg)
