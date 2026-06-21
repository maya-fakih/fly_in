"""Custom exceptions raised during configuration parsing."""

from typing import Optional


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

    def __init__(self, line: Optional[object] = None) -> None:
        """Initialize DroneNumberError, optionally including a line number."""
        msg = '[Parsing Error]: Invalid drone number'
        if line is not None:
            msg = f'{msg}. Error at line {line}'
        super().__init__(msg)


class TypesError(ParsingError):
    """Raised when the data type is wrong."""

    def __init__(self, msg: str = '[Parsing Error]: Invalid data.') -> None:
        """Initialize TypesError with an optional message."""
        super().__init__(msg)


class IntTypeError(TypesError):
    """Raised when the expected type is int but does not comply."""

    def __init__(self, line: Optional[object] = None) -> None:
        """Initialize IntTypeError, optionally including a line number."""
        msg = '[Parsing Error]: Not a valid integer'
        if line is not None:
            msg = f'{msg}. Error at line {line}'
        super().__init__(msg)


class NameTypeError(TypesError):
    """Raised when the hub name line is malformed."""

    def __init__(self, line: Optional[object] = None) -> None:
        """Initialize NameTypeError, optionally including a line number."""
        msg = '[Parsing Error]: Invalid Hub name'
        if line is not None:
            msg = f'{msg}. Error at line {line}'
        super().__init__(msg)


class ConnectionTypeError(TypesError):
    """Raised when the connection line is malformed."""

    def __init__(self, line: Optional[object] = None) -> None:
        """Initialize ConnectionTypeError, optionally including a \
        line number."""
        msg = '[Parsing Error]: Invalid Connection'
        if line is not None:
            msg = f'{msg}. Error at line {line}'

        super().__init__(msg)


class MetaDataTypeError(TypesError):
    """Raised when the metadata line is malformed."""

    def __init__(self, line: Optional[object] = None) -> None:
        """Initialize MetaDataTypeError, optionally including a line number."""
        msg = '[Parsing Error]: Invalid Metadata'
        if line is not None:
            msg = f'{msg}. Error at line {line}'
        super().__init__(msg)


class HubTypeError(TypesError):
    """Raised when the hub type is invalid (start_hub, end_hub, hub)."""

    def __init__(self, line: Optional[object] = None) -> None:
        """Initialize HubTypeError, optionally including a line number."""
        base = (
            '[Parsing Error]: Invalid hub type should be '
            'start_hub, end_hub, or hub'
        )
        if line is not None:
            base = f'{base}. Error at line {line}'
        super().__init__(base)


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


class ColorFormat(FormatError):
    """Raised for hub-color formatting errors."""

    def __init__(self, line: str) -> None:
        """Initialize color with offending line."""
        msg = (
            '[Parsing Error]: color is invalid'

            f'Error at line: {line}'

        )
        super().__init__(msg)


class DuplicateError(ParsingError):
    """Raised when the data is duplicated."""

    def __init__(self, msg: str = '[Parsing Error]: Duplicated data.') -> None:
        """Initialize TypesError with an optional message."""
        super().__init__(msg)


class NameDuplicateError(DuplicateError):
    """Raised when the hub name already exists."""

    def __init__(self, line: Optional[object] = None) -> None:
        """Initialize NameDuplicateError, optionally including a line."""
        msg = '[Parsing Error]: Duplicate Hub name'
        if line is not None:
            msg = f'{msg}. Error at line {line}'
        super().__init__(msg)


class CoordsDuplicateError(DuplicateError):
    """Raised when the hub has duplicate coords or the line is malformed."""

    def __init__(self, line: Optional[object] = None) -> None:
        """Initialize coord error, optionally including a line number."""
        msg = '[Parsing Error]: Invalid coordinates'
        if line is not None:
            msg = f'{msg}. Error at line {line}'
        super().__init__(msg)


class DuplicateZone(DuplicateError):
    """Raised when the map has duplicate start or end zones."""

    def __init__(self, line: Optional[object] = None) -> None:
        """Initialize duplicate start-end hubs."""
        msg = '[Parsing Error]: You cannot have more than one start/end hub'
        if line is not None:
            msg = f'{msg}. Error at line {line}'
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
    'NameDuplicateError',
    'DuplicateZone',
    'ConnectionTypeError',
]
