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

class TypesError(ParsingError):
    """Raised when the data type is wrong"""

    def __init__(self):
        """Initialize the data error with a standard message."""
        msg = '[Parsing Error]: Invalid data type.'
        super().__init__(msg)

class IntTypeError(TypesError):
    """Raised when the expected type is int but doesnt comply"""

    def __init__(self):
        """Initialize the int number error with a standard message."""
        msg = '[Parsing Error]: Not a valid integer'
        super().__init__(msg)

class NameTypeError(TypesError):
    """Raised when the hub name line is malformed."""

    def __init__(self):
        """Initialize the hub name error with a standard message."""
        msg = '[Parsing Error]: Invalid Hub name'
        super().__init__(msg)

class MetaDataTypeError(TypesError):
    """Raised when the metadata line is malformed."""

    def __init__(self):
        """Initialize the meta data error with a standard message."""
        msg = '[Parsing Error]: Invalid Metadata'
        super().__init__(msg)

class CoordinatesTypeError(TypesError):
    """Raised when the hub has duplicate coordinates or line is malformed."""

    def __init__(self):
        """Initialize the hub coordinates error with a standard message."""
        msg = '[Parsing Error]: Invalid coordinates'
        super().__init__(msg)

class FormatError(ParsingError):
    """Raised when input format is invalid."""

    def __init__(self, line):
        """Fromat error in config maze files."""
        e = 'Line should be of format key: value.'
        msg = f'[Parsing Error]: {e} Error at line: {line}'
        super().__init__(msg)

class HubFormat(FormatError):
    """Child class to fromat errors"""

    def __init__(self, line):
        """Error in formatting the hub lines"""
        e = f'Line should be of form {f}'
        f = 'hub: name x y [color=... max_drones=... zone=...]'
        msg = f'[Parsing Error]: {e}. Error at line: {line}'