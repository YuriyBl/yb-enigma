"""
Rotor class
"""
from random import shuffle

from .common import ALPH
from .exceptions import NotFound


class Rotor:
    """Rotor class.

    Args:
        pos (int):    Initial position (rotation step).
        key (str):    Alphabet permutation (more in documentation).
        num (str):    Rotor's num.
        debug (bool): Debug mode

    Attributes:
        debug (bool):            Debug mode.
        next_rotor (Rotor):      The next rotor.
        prev_rotor (Rotor):      The previous rotor.
        num (str):               Number
        pos (int):               Current position (rotation step).
        coding_list (list[int]): Coding list (more in documentation).

    """

    def __init__(self, pos=0, key=None, num='', debug=False):
        self.debug = debug

        self.next_rotor = None  # pointer to next rotor, if any
        self.prev_rotor = None  # pointer to previous rotor, if any

        self.num = num          # rotor's number (e.g. I, II, ..., VIII)
        self.pos = pos          # position (rotation step)

        # if key was not provided, use random permutation of alphabet
        key = key if key is not None else shuffle(ALPH.copy())
        self.coding_list = []
        for char in key:
            self.coding_list.append(ALPH.index(char))  # creating coding_list (more in documentation).

    def __str__(self):
        return self.num+':'+str(self.pos)

    def encode(self, char: str, reverse: bool = False):
        """Encode char.
        Described in "Docs -> How it works -> Rotor"

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

        if reverse:
            encoded_char = ALPH[(self.coding_list.index(ALPH.index(char)) - self.pos) % 26]
        else:
            encoded_char = ALPH[self.coding_list[(ALPH.index(char) + self.pos) % 26]]

        if self.debug:
            print(f'  Rotor {self.num} | {char} => {encoded_char} | pos => {self.pos} | {reverse}')

        # pass encoded letter to the next (previous if reverse) rotor
        if reverse and self.prev_rotor is not None:
            return self.prev_rotor.encode(encoded_char, reverse=True)
        if not reverse and self.next_rotor is not None:
            return self.next_rotor.encode(encoded_char)

        return encoded_char

    def shift(self):
        """Shift rotors position by 1.

        Args:
            None

        Return:
            None
        """
        self.pos += 1
        if self.pos > 25:
            # if full rotation was made, reset position to 0 and rotate next rotor, if any
            self.pos = 0
            if self.next_rotor is not None:
                self.next_rotor.shift()

    @staticmethod
    def I(pos=0, debug=False):
        """Rotor I"""
        return Rotor(pos=pos, key='ekmflgdqvzntowyhxuspaibrcj', num='I', debug=debug)

    @staticmethod
    def II(pos=0, debug=False):
        """Rotor II"""
        return Rotor(pos=pos, key='wyhxuspaibrcjekmflgdqvznto', num='II', debug=debug)

    @staticmethod
    def III(pos=0, debug=False):
        """Rotor III """
        return Rotor(pos=pos, key='bdfhjlcprtxvznyeiwgakmusqo', num='III', debug=debug)

    @staticmethod
    def IV(pos=0, debug=False):
        """Rotor IV"""
        return Rotor(pos=pos, key='esovpzjayquirhxlnftgkdcmwb', num='IV', debug=debug)

    @staticmethod
    def V(pos=0, debug=False):
        """Rotor V"""
        return Rotor(pos=pos, key='vzbrgityupsdnhlxawmjqofeck', num='V', debug=debug)

    @staticmethod
    def VI(pos=0, debug=False):
        """Rotor VI"""
        return Rotor(pos=pos, key='jpgvoumfyqbenhzrdkasxlictw', num='VI', debug=debug)

    @staticmethod
    def VII(pos=0, debug=False):
        """Rotor VII"""
        return Rotor(pos=pos, key='nzjhgrcxmyswboufaivlpekqdt', num='VII', debug=debug)

    @staticmethod
    def VIII(pos=0, debug=False):
        """Rotor VIII"""
        return Rotor(pos=pos, key='fkqhtlxocbjspdzramewniuygv', num='VIII', debug=debug)

    @staticmethod
    def by_num(num: str, pos: int = 0, debug: bool = False):
        """Get Rotor by num.

        Args:
            num (str):    Rotors number (I, II, ..., VIII).
            pos (int):    Initial position.
            debug (bool): Debug mode

        Returns:
            Rotor: Rotor instance

        Raises:
            NotFound: If rotor with such "num" was not found
        """
        if num == 'I':
            return Rotor.I(pos=pos, debug=debug)
        if num == 'II':
            return Rotor.II(pos=pos, debug=debug)
        if num == 'III':
            return Rotor.III(pos=pos, debug=debug)
        if num == 'IV':
            return Rotor.IV(pos=pos, debug=debug)
        if num == 'V':
            return Rotor.V(pos=pos, debug=debug)
        if num == 'VI':
            return Rotor.VI(pos=pos, debug=debug)
        if num == 'VII':
            return Rotor.VII(pos=pos, debug=debug)
        if num == 'VIII':
            return Rotor.VIII(pos=pos, debug=debug)

        raise NotFound(f'Rotor "{num}"')

    @staticmethod
    def list():
        """Get list of all available rotors.

        Args:
            None

        Returns:
            list[Rotor]: List of all available rotors.
        """
        return [
            Rotor.I(),
            Rotor.II(),
            Rotor.III(),
            Rotor.IV(),
            Rotor.V(),
            Rotor.VI(),
            Rotor.VII(),
            Rotor.VIII(),
        ]
