"""
Enigma emulator

Classes:

    Enigma
    Rotor
    Reflector
    Plugboard

Functions:

    parse_configuration
    format_output_string
    keep_only_alph
    prepare_string


Initialize by:
    from yb_enigma import *
    1. use default configuration "A I-II"
       enigma = Enigma()
    2. use random configuration
       enigma = Enigma(random_cngf: True)
    3. use parsed configuration string
       reflector, rotors_list, plugboard = parse_configuration(configuration_string)
       enigma = Enigma(
           reflector   = reflector,
           rotors_list = rotors_list,
           plugboard   = plugboard,
       )
    4. use manual configuration
       reflector = Reflector.A()
       rotors_list = [Rotor.I(pos=2), Rotor.II(pos=10), Rotor.III(pos=0)]
       plugboard = Plugboard(pairs=[{'a', 'b'}, {'c', 'd'}])
       // above is equal to: reflector, rotors_list, plugboard = parse_configuration("A I:2-II:10-III:0 AB:CD")
       enigma = Enigma(
           reflector   = reflector,
           rotors_list = rotors_list,
           plugboard   = plugboard,
       )

Get current configuration as configuration string:
    cnfg_string = enigma.get_configuration()

Encode string:
    // using 'save_state' parameter, you can define if enigma`s state will be changed after encoding, or saved as it was before
    encoded_string = enigma.encode('hello world', save_state=False)

Set configuration by configuration string:
    enigma.set_configuration(cnfg_string)

Decode string:
    decoded_string = enigma.encode(encoded_string)
"""

from .utils import *
from .enigma import *
from .rotor import *
from .reflector import *
from .plugboard import *
from .exceptions import *
from .common import *
