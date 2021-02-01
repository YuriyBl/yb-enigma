"""
Utils
"""
import re
from .reflector import Reflector
from .rotor import Rotor
from .plugboard import Plugboard
from .exceptions import InvalidConfigurationString, InvalidPlugboardPair


def parse_configuration(conf_str: str, debug=False):
    """Parse configuration string

    Args:
        conf_str (str): Configuration string to validate.

    Returns:
        tuple[Plugboard, list[Rotor], Plugboard]: parsed configuration

    Raises:
        (see 'validate_configuration_string')
    """
    conf_str = conf_str.strip()
    validate_configuration_string(conf_str)

    conf = conf_str.split(' ')

    reflector = Reflector.by_num(conf[0], debug=debug)

    rotors_list = []
    for rotor_conf in conf[1].split('-'):
        rotor_conf = rotor_conf.split(':')
        rotor_num = rotor_conf[0]
        rotor_pos = int(rotor_conf[1]) if len(rotor_conf) > 1 else 0
        rotors_list.append(Rotor.by_num(num=rotor_num, pos=rotor_pos, debug=debug))

    plugboard = Plugboard()
    if len(conf) > 2 and conf[2] != '':
        for plug_pair in conf[2].split(':'):
            i, j = plug_pair[0].lower(), plug_pair[1].lower()
            if i == j:
                raise InvalidPlugboardPair()
            plugboard.plug({i, j})

    return reflector, rotors_list, plugboard


def validate_configuration_string(conf_str: str):
    """Configuration string validator

    Args:
        conf_str (str): Configuration string to validate.

    Returns:
        None

    Raises:
        InvalidConfigurationString: if configuraiton string is invalid
    """
    if not conf_str or conf_str == '':
        raise InvalidConfigurationString()

    conf = conf_str.split(' ')
    if len(conf) < 2 or len(conf) > 3:
        raise InvalidConfigurationString()

    if conf[0] == '' or conf[0] not in [reflector.num for reflector in Reflector.list()]:
        raise InvalidConfigurationString()

    if conf[1] == '':
        raise InvalidConfigurationString()

    rotor_confs = conf[1].split('-')
    for rotor_conf in rotor_confs:
        if not re.fullmatch(r"^(I|II|III|IV|V|VI|VII|VIII)(\:((1[0-9]?)|(2[0-6]?)|([0-9])))?$", rotor_conf):
            raise InvalidConfigurationString()

    if len(conf) == 3:
        if conf[2] == '':
            raise InvalidConfigurationString()

        pairs = conf[2].split(':')
        for pair in pairs:
            if not re.fullmatch(r"^([A-Z]{2})$", pair):
                raise InvalidConfigurationString()


def format_output_string(string: str, max_char_num=5):
    """Format string, as people used to do with real Enigma

    Args:
        string (str):           String to format
        max_char_num (int):     Num of chars in one 'block',
                                i.e. max_char_num = 4; "helloworld" => 'HELL OWOR LD'

    Returns:
        formated_string (str):  Formatted string
    """
    result_string = ''
    for i, char in enumerate(string):
        if i % max_char_num == 0 and i != 0:
            result_string += ' '
        result_string += char.upper()

    return result_string


def keep_only_alph(string: str):
    """Format string, keeping only alphs

    Args:
        string (str):           String to format

    Returns:
        formated_string (str):  Formatted string
    """
    return re.sub('[^a-zA-Z]+', '', string)


def prepare_string(string: str):
    """Format string, keeping only lower-cased eng alph chars, without spaces

    Args:
        string (str):           String to format

    Returns:
        formated_string (str):  Formatted string
    """
    return keep_only_alph(string).lower().replace(' ', '')
