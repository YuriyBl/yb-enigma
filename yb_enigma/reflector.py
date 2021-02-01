"""
Reflector class
"""
from .common import ALPH
from .exceptions import NotFound


class Reflector:
    """Reflector class.

    Args:
        key (str):    Special alphabet permutation (more in documentation).
        num (str):    Reflectors's num.
        debug (bool): Debug mode

    Attributes:
        debug (bool):            Debug mode.
        num (str):               Number
        coding_list (list[int]): Coding list (more in documentation).
    """

    def __init__(self, key: str = '', num: str = '', debug: bool = False):
        self.debug = debug

        self.num = num
        key = list(key)
        self.coding_list = []
        for char in key:
            self.coding_list.append(ALPH.index(char))

    def __str__(self):
        return self.num

    def encode(self, char: str):
        """Encode char.
        Described in "Docs -> How it works -> Reflector"

        Args:
            char (str):     Char to encode.
            reverse (bool): Reverse (more in documentation).

        Returns:
            str: Encoded char.

        Raises:
            ValueError: If length of 'char' is not 1.
        """
        if len(char) != 1:
            raise ValueError('"char" length must be 1')

        encoded_char = ALPH[self.coding_list[ALPH.index(char)]]

        if self.debug:
            print(f'  Reflector {self.num} | {char} => {encoded_char}')

        return encoded_char

    @staticmethod
    def A(debug=False):
        """Reflector A"""
        return Reflector(key='ejmzalyxvbwfcrquontspikhgd', num='A', debug=debug)

    @staticmethod
    def B(debug=False):
        """Reflector B"""
        return Reflector(key='yruhqsldpxngokmiebfzcwvjat', num='B', debug=debug)

    @staticmethod
    def C(debug=False):
        """Reflector C"""
        return Reflector(key='fvpjiaoyedrzxwgctkuqsbnmhl', num='C', debug=debug)

    @staticmethod
    def by_num(num: str, debug=False):
        """Get reflector by its num.

        Args:
            num (str):    Reflector's number (A, B, C).
            debug (bool): Debug mode

        Returns:
            Reflector: Reflector instance

        Raises:
            NotFound: If reflector with such "num" was not found

        """
        if num == "A":
            return Reflector.A(debug=debug)
        if num == "B":
            return Reflector.B(debug=debug)
        if num == "C":
            return Reflector.C(debug=debug)

        raise NotFound(f'Reflector "{num}"')

    @staticmethod
    def list():
        """List of all available reflectors.

        Args:
            None

        Returns:
            list[Reflector]: List of all available reflectors.
        """
        return [
            Reflector.A(),
            Reflector.B(),
            Reflector.C(),
        ]
