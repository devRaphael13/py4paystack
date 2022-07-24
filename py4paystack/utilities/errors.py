class Error(Exception):
    """Base class for other exceptions"""

class UnwantedArgumentsError(Error):
    """raised when a dealing with unwanted arguments
    """

class MissingArgumentsError(Error):
    """raised when an argument is missing
    """
