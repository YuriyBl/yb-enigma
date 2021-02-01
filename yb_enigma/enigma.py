"""
Enigma class
"""
import random
from .rotor import Rotor
from .reflector import Reflector
from .plugboard import Plugboard

from .utils import parse_configuration, prepare_string

DEFAULT_ROTORS_LIST = [Rotor.I(), Rotor.II()]
DEFAULT_REFLECTOR = Reflector.A()
DEFAULT_PLUGBOARD = Plugboard()


class Enigma:
    """Enigma class.

    Args:
        random_cnfg (bool):    Use random configuration.
        rotors (list[Rotor]):  List of rotors.
        reflector (Reflector): Reflector.
        plugboard (Plugboard): Plugboard.
        debug (bool):          Enable debug mode

    Attributes:
        debug (bool): Debug mode.
        first_rotor (Rotor):   The first rotor.
        last_rotor (Rotor):    The last rotor.
        reflector (Reflector): Reflector.
        plugboard (Plugboard): Plugboard.

    """

    def __init__(self, random_cnfg: bool = False, rotors: list[Rotor] = None, reflector: Reflector = None, plugboard: Plugboard = None, debug: bool = False):
        self.debug = debug
        self.first_rotor = None
        self.last_rotor = None

        if random_cnfg:
            self.set_random_configuration()
        else:
            rotors = rotors if rotors is not None else DEFAULT_ROTORS_LIST
            reflector = reflector if reflector is not None else DEFAULT_REFLECTOR
            plugboard = plugboard if plugboard is not None else DEFAULT_PLUGBOARD

            self.create_rotors_dll(rotors)

            self.reflector = reflector
            self.plugboard = plugboard

    def create_rotors_dll(self, rotors_list: list[Rotor]):
        """Create doubly linked list of rotors.

        Args:
            rotors_list (list[Rotor]): List of rotors.

        Returns:
            None

        Raises:
            ValueError: If 'rotors_list' is empty.
        """

        if len(rotors_list) == 0:
            raise ValueError('Empty rotors list')

        self.first_rotor = None
        self.last_rotor = None

        rotors_list.reverse()
        prev_rotor = rotors_list[0]
        for rotor in rotors_list:
            if self.first_rotor is None:
                self.first_rotor = rotor
            else:
                rotor.prev_rotor = prev_rotor
                prev_rotor.next_rotor = rotor

            prev_rotor = rotor

        self.last_rotor = prev_rotor

    def get_rotors_list(self, reverse: bool = False):
        """Create ordinary list from doubly linked list of rotors.

        Args:
            reverse (bool): Reverse list.

        Returns:
            list[Rotor]: List of rotors.
        """
        if self.first_rotor is None or self.last_rotor is None:
            return []

        rotors_list = []
        if reverse:
            rotor = self.last_rotor
            while rotor is not None:
                rotors_list.append(rotor)
                rotor = rotor.prev_rotor
        else:
            rotor = self.first_rotor
            while rotor is not None:
                rotors_list.append(rotor)
                rotor = rotor.next_rotor
        return rotors_list

    def get_configuration(self):
        """Get current configuration string (more about "configuration string" in documentation).

        Returns:
            string: Configuration string (more in documentation).
        """
        reflector_num = self.reflector.num

        rotor = self.last_rotor
        rotors_conf = []
        while rotor is not None:
            rotors_conf.append(rotor.num + ':' + str(rotor.pos))
            rotor = rotor.prev_rotor
        rotors_conf_str = '-'.join(rotors_conf)

        plugboard_conf = self.plugboard.get_pairs_string()

        if plugboard_conf == '':
            return ' '.join([reflector_num, rotors_conf_str])
        else:
            return ' '.join([reflector_num, rotors_conf_str, plugboard_conf])

    def set_configuration(self, conf_str: str):
        """Set configuraion by configuration string.

        Args:
            conf_str (str): Configuration string (more in documentation).

        Returns:
            None
        """
        reflector, rotors_list, plugboard = parse_configuration(conf_str, debug=self.debug)
        self.create_rotors_dll(rotors_list)
        self.reflector = reflector
        self.plugboard = plugboard

    def set_random_configuration(self, rotors_amount: int = 3, plugpairs_amount: int = 6):
        """Set random rotors, reflector and plugboard configuration.

        Args:
            rotors_amount (int):    Amount of rotors.
            plugpairs_amount (int): Amount of plugpairs.

        Returns:
            None
        """
        available_rotors_list = Rotor.list()
        rotors_list = []
        for _ in range(rotors_amount):
            rotor = random.choice(available_rotors_list)
            rotor.debug = self.debug
            rotor.pos = random.randint(0, 24)
            rotors_list.append(rotor)
            available_rotors_list.remove(rotor)

        self.create_rotors_dll(rotors_list)
        self.reflector = random.choice(Reflector.list())
        self.reflector.debug = self.debug
        self.plugboard = Plugboard()
        self.plugboard.debug = self.debug
        for _ in range(plugpairs_amount):
            self.plugboard.plug_random()

    def _encode_char(self, char: str):
        """Encode char.

        Args:
            char (int): Char to encode.

        Returns:
            str: Encoded char.

        Raises:
            ValueError: If length of 'char' is not 1.
        """
        if len(char) != 1:
            raise ValueError('"char" length must be 1')

        self.first_rotor.shift()                                    # shift (rotate by 1) the first rotor

        encoded_char = self.plugboard.encode(char)                  # through plugboard
        encoded_char = self.first_rotor.encode(encoded_char)        # through all rotors 1-N
        encoded_char = self.reflector.encode(encoded_char)          # thorugh reflector
        encoded_char = self.last_rotor.encode(encoded_char, True)   # through all rotors N-1
        encoded_char = self.plugboard.encode(encoded_char)          # through plugboard

        if self.debug:
            print(f'Encoded "{char}" to "{encoded_char}" \n')

        return encoded_char

    def encode(self, string: str = '', save_state: bool = False):
        """Encode string.

        Args:
            string (str):      String to encode.
            save_state (bool): Save state after encoding

        Returns:
            str: Encoded string.
        """
        if save_state:
            cnfg_string = self.get_configuration()

        encoded_string = ''
        for char in prepare_string(string):
            encoded_string += self._encode_char(char)

        if save_state:
            self.set_configuration(cnfg_string)

        return encoded_string
