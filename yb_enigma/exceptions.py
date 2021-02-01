"""
Custom exceptions.
"""


class NotFound(Exception):
    """Not found exception.

    Args:
        instance (str): string, representing what was not found
    """

    def __init__(self, instance: str):
        Exception.__init__(self, f'{instance}" not found')


class InvalidConfigurationString(Exception):
    """Invalid configuration string exception.

    Args:
        None
    """

    def __init__(self):
        Exception.__init__(self, 'Invalid configuration string! Use "main.py -h-cnfg" to view examples')


class InvalidPlugboardPair(Exception):
    """Invalid plugpair exception.

    Args:
        msg (str): Error explanation
    """

    def __init__(self, msg: str = 'Unknown error'):
        Exception.__init__(self, f'Invalid plugboard pair: {msg}')


class NotUniquePair(Exception):
    """Not unique plugpair exception.

    Args:
        None
    """

    def __init__(self):
        Exception.__init__(self, 'Only unique pairs')


class InvalidArguments(Exception):
    """Invalid arguments exception.

    Args:
        msg (str): Error explanationone
    """

    def __init__(self, msg: str = 'Unknown arguments error'):
        Exception.__init__(self, f'Arguments error: {msg}')
