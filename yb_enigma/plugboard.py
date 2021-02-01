"""
Plugboard class
"""
import random
from .common import ALPH
from .exceptions import NotUniquePair, InvalidPlugboardPair


class Plugboard():
    """Plugboard.

    Note: plugbair is set of 2 lowercase letters.

    Args:
        pairs (list[set[str, str]]): Initial plugpairs.
        debug (bool): Debug mode.

    Attributes:
        pairs (list[set[str, str]]): Plugpais list.
        debug (bool): Debug mode.
    """

    def __init__(self, pairs: list[set] = None, debug=False):
        self.debug = debug
        self.pairs = []
        if pairs:
            for pair in pairs:
                self.plug(pair)

    def __str__(self):
        return self.get_pairs_string()

    def _letter_in_pairs(self, letter: str):
        """Check if letter is already in pairs.

        Args:
            letter (str): Letter to check.

        Returns:
            bool: True if letter is already in pairs, False otherwise.
        """
        for pair in self.pairs:
            if letter in pair:
                return True
        return False

    def plug(self, pair: set):
        """Add plugpair to list.

        Args:
            pair (set[str, str]): Plugpair (set of 2 lowercase letters).

        Returns:
            None

        Raises:
            InvalidPlugboardPair: If invalid plugpair was passed.
            NotUniquePair: If one of pair's letters is already in pairs list.
        """
        if len(pair) != 2:
            raise InvalidPlugboardPair('"pair" length must be 2')

        i, j = pair
        if i == j:
            raise InvalidPlugboardPair('same letters')

        # check if any letter from new pair is already "plugged"
        if self._letter_in_pairs(i) or self._letter_in_pairs(j):
            raise NotUniquePair()

        self.pairs.append(pair)

    def unplug(self, pair: set):
        """Remove pair of letters.

        Args:
            pair (set[str, str]): Plugpair to unplug.

        Returns:
            None
        """
        if pair in self.pairs:
            self.pairs.remove(pair)

    def plug_random(self):
        """Plug random plugpair.

        Args:
            None

        Returns:
            bool: True if new plugpair was plugged, False if it's not possible.
        """
        letters = ALPH.copy()  # available letters list

        # remove letters, that are already in plugged pairs
        for i, j in self.pairs:
            letters.remove(i)
            letters.remove(j)

        # return False, if no available letters left
        if len(letters) == 0:
            return False

        first_letter = random.choice(letters)   # choose random letter from available
        letters.remove(first_letter)            # remove chosen letter from available list
        second_letter = random.choice(letters)  # choose second letter from available

        self.pairs.append({first_letter, second_letter})
        return True

    def get_pairs_string(self):
        """Get plugpairs list as string.

        Used as part of Configuration string.

        Args:
            None

        Returns:
            str: Plugpairs list as string.
        """
        return ':'.join((i+j).upper() for i, j in self.pairs)

    def encode(self, char: str):
        """Encode char.
        Described in "Docs -> How it works -> Plugboard"

        Args:
            char (str):     Char to encode.
            reverse (bool): Reverse (more in documentation).

        Returns:
            str: Encoded char (the same char if it's not in any of plugpairs).

        Raises:
            ValueError: If length of 'char' is not 1.
        """
        if len(char) != 1:
            raise ValueError('"char" length must be 1')

        for i, j in self.pairs:     # go through each plugged pair
            if char == i:
                encoded_char = j    # get corresponding letter
                break
            if char == j:           # get corresponding letter
                encoded_char = i
                break
        else:
            encoded_char = char     # return the char itself, if not found in pairs

        if self.debug:
            print(f'  Plugboard | {char} => {encoded_char}')

        return encoded_char
