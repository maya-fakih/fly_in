"""Custom exceptions raised during configuration parsing."""


class ParsingError(Exception):
    """Base exception for parsing errors.

    The exception accepts an optional message so child classes can provide
    specific error details.
    """

    def __init__(self, msg: str = '[Parsing Error]: Invalid input') -> None:
        """Initialize the base parsing error with an optional message."""
        super().__init__(msg)


class DroneNumberError(ParsingError):
    """Raised when the drone number line is malformed."""

    def __init__(self) -> None:
        """Initialize DroneNumberError."""
        super().__init__('[Parsing Error]: Invalid drone number')


class TypesError(ParsingError):
    """Raised when the data type is wrong."""

    def __init__(self, msg: str = '[Parsing Error]: Invalid data.') -> None:
        """Initialize TypesError with an optional message."""
        super().__init__(msg)


class IntTypeError(TypesError):
    """Raised when the expected type is int but does not comply."""

    def __init__(self) -> None:
        """Initialize IntTypeError."""
        super().__init__('[Parsing Error]: Not a valid integer')


class NameTypeError(TypesError):
    """Raised when the hub name line is malformed."""

    def __init__(self) -> None:
        """Initialize NameTypeError."""
        super().__init__('[Parsing Error]: Invalid Hub name')


class MetaDataTypeError(TypesError):
    """Raised when the metadata line is malformed."""

    def __init__(self) -> None:
        """Initialize MetaDataTypeError."""
        super().__init__('[Parsing Error]: Invalid Metadata')


class CoordinatesTypeError(TypesError):
    """Raised when the hub has duplicate coords or the line is malformed."""

    def __init__(self) -> None:
        """Initialize CoordinatesTypeError."""
        super().__init__('[Parsing Error]: Invalid coordinates')


class HubTypeError(TypesError):
    """Raised when the hub type is invalid (start_hub, end_hub, hub)."""

    def __init__(self) -> None:
        """Initialize HubTypeError."""
        msg = (
            '[Parsing Error]: Invalid hub type should be '
            'start_hub, end_hub, or hub'
        )
        super().__init__(msg)


class FormatError(ParsingError):
    """Raised when input format is invalid."""

    def __init__(self, line: str) -> None:
        """Initialize FormatError with offending line."""
        e = 'Line should be of format key: value.'
        msg = (
            f'[Parsing Error]: {e} '
            f'Error at line: {line}'
        )
        super().__init__(msg)


class HubFormat(FormatError):
    """Raised for hub-specific formatting errors."""

    def __init__(self, line: str) -> None:
        """Initialize HubFormat with offending line."""
        msg = (
            '[Parsing Error]: Line should be of form '
            'hub: name x y [color=... max_drones=... zone=...]. '
            f'Error at line: {line}'
        )
        super().__init__(msg)


# Public API for from ... import *
__all__ = [
    'ParsingError',
    'DroneNumberError',
    'TypesError',
    'IntTypeError',
    'NameTypeError',
    'MetaDataTypeError',
    'CoordinatesTypeError',
    'HubTypeError',
    'FormatError',
    'HubFormat',
]
