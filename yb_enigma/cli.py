"""
ENIGMA
Yurii Bliusiuk, I. rocnik
Zimni semestr 2020
Programovani I (NPRG030)

Entry point for console application.
"""

import argparse
import textwrap
import os
import sys

from .utils import parse_configuration, format_output_string
from .exceptions import InvalidArguments
from .enigma import Enigma


def run():
    """
    CLI entry point.
    """
    parser = argparse.ArgumentParser(
        prog="Enigma CLI",

        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("--help-configuration", "-h-cnfg",
                        action="store_true",
                        help='Show configuration string help message.')

    parser.add_argument("--string", "-s",
                        help='String to encode.')

    parser.add_argument("--input-file", "-f",
                        type=argparse.FileType('r'),
                        help=textwrap.dedent('''\
                            Path to source file. '''))

    parser.add_argument("--key-file", "-k",
                        type=argparse.FileType('r'),
                        help=textwrap.dedent('''\
                            Path to key file. '''))

    parser.add_argument("--output-file", "-o",
                        type=argparse.FileType('w'),
                        help=textwrap.dedent('''\
                            Path to destination file.
                            If (--save-key, -sk) - key will be saved to /path/to/destination_file_name.key '''))

    parser.add_argument("--configuration", "-cnfg",
                        help=textwrap.dedent('''\
                            Set enigma configurations.
                            Format:  '[rf_num] [rt1_num]:[rt1_pos]-[rt2_num]:[rt2_pos]-...-rtN_num]:[rtN_pos] [pl1]:[pl2]:...:[plN]'
                                - rf: reflector
                                - rt: rotor
                                - pl: plugboard pair
                            Example: 'A II:10-I:3-III:20 AB:CD:XZ:GE' '''))

    parser.add_argument("--random-configuration", "-rcnfg",
                        help='Set random rotors, reflector and plugboard configuration.',
                        action="store_true")

    parser.add_argument("--keep-spaces", "-ks",
                        help='Keep spaces in input string.',
                        action="store_true")

    parser.add_argument("--keep-special", "-kx",
                        help='Keep all special characters in input string.',
                        action="store_true")

    parser.add_argument("--keep-new-line", "-kn",
                        help='Keep new line charecters in input string.',
                        action="store_true")

    parser.add_argument("--groups", "-g",
                        help=textwrap.dedent("""\
                        Divide output string to groups.
                        Example: "ENIGMA IS COOL" => "ENIGM AISCO OL"
                        Can`t be used with '--keep-spaces', '--keep-special' or '--keep-new-line'"""),
                        action="store_true")

    parser.add_argument("--save-key", "-sk",
                        help='Enable debug output.',
                        action="store_true")

    parser.add_argument("--debug", "-d",
                        help='Enable debug output.',
                        action="store_true")

    args = parser.parse_args()

    # Show configuration string help message
    if bool(args.help_configuration):
        print(textwrap.dedent("""\

        Configuration string: string, containing valid enigma machine configuration.

        For example: A II:10-I:3-III:20 AB:CD
            1) A - reflector
            2) II:10-I:3-III:20 - rotors
                a) II:10 - set first rotor to II at position 10
                b) I:3 - set second rotor to I at position 3
                c) III:20 - set third rotor to III at position 20
            3) AB:CD - plugboard
                a) AB - Plug pair A to B
                b) CD - Plpug pair C to D
        
        Valid configuration string examples:
            1) A II:10-I:3-III:20 AB:CD
            2) A II:10-I:3-III:20
            3) A II-I-III ( == A II:0-I:0-III:0)
            4) A I-I-I
            5) B IV
            6) C V:25

        Invalid configuration string examples:
            1) II:10-I:3-III:20 AB:CD (reflector must be specified)
            2) A I:30-II:0 (30 >= 26)
            3) A I-II-III AA (invalid plugboard pair - same letters)
            4) C I-II-III AB:BD (invalid plugboard pair - same letter is used multiple times)
        """))
        sys.exit(0)

    # Debug mode
    debug = bool(args.debug)

    # Neither string nor file provided as input source
    if not args.string and not args.input_file:
        raise InvalidArguments('Specify some input sourse: string(-s, --string) or file(-i, --input-file)')

    # Both string and file provided as input source
    if args.string and args.input_file:
        raise InvalidArguments('Can\'t use both string(-s, --string) and file(-i, --input-file) input source')

    # Both random and defined configuration
    if args.random_configuration and args.configuration:
        raise InvalidArguments('Can\'t use both random and defined configuration')

    # Both random and key file configuration
    if args.random_configuration and args.key_file:
        raise InvalidArguments('Can\'t use both random and defined configuration from file')

    # Both defilned and key file configuration
    if args.configuration and args.key_file:
        raise InvalidArguments('Can\'t use both defined configuration by string and defined configuration from file')

    if (args.keep_spaces or args.keep_new_line or args.keep_special) and args.groups:
        raise InvalidArguments('Can\'t use division into groups with "--keep-spaces", "--keep-special" or "--keep-new-line"')

    # INITIALISATION
    rotors_list, reflector, plugboard = None, None, None

    # if configuration is given by string or file, parse it and use in enigma initialisation
    if args.configuration:
        reflector, rotors_list, plugboard = parse_configuration(args.configuration, debug=debug)
    elif args.key_file:
        reflector, rotors_list, plugboard = parse_configuration(args.key_file.readline(), debug=debug)

    enigma = Enigma(rotors=rotors_list,
                    reflector=reflector,
                    plugboard=plugboard,
                    random_cnfg=bool(args.random_configuration),
                    debug=debug)

    # save current configuration string
    conf_string = enigma.get_configuration()
    encoded_string = ''

    # FILE MODE
    if args.input_file:
        # read and encode char by char
        char = args.input_file.read(1)
        while char:
            # if char is alph, encode it anyway
            if char.isalpha():
                encoded_string += enigma.encode(char)
            # if it's space, keep it only if "-ks, --keep-spaces" was set
            elif char == ' ':
                if args.keep_spaces:
                    encoded_string += char
            # if it's new line char, keep it only if "-kn, --keep-new-line" was set
            elif char == '\n':
                if args.keep_new_line:
                    encoded_string += char
            # if it's smth else, keep it only if "-kx, --keep-special" was set
            elif args.keep_special:
                encoded_string += char

            char = args.input_file.read(1)

        args.input_file.close()

    # STRING MODE
    elif args.string:
        # encode char by char
        for char in args.string:
            # if char is alph, encode it anyway
            if char.isalpha():
                encoded_string += enigma.encode(char)
            # if it's space, keep it only if "-ks, --keep-spaces" was set
            elif char == ' ':
                if args.keep_spaces:
                    encoded_string += char
            # if it's new line char, keep it only if "-kn, --keep-new-line" was set
            elif char == '\n':
                if args.keep_new_line:
                    encoded_string += char
            # if it's smth else, keep it only if "-kx, --keep-special" was set
            elif args.keep_special:
                encoded_string += char

    # OUTPUT
    if args.output_file:
        # format encoded string, if needed
        if args.groups:
            encoded_string = format_output_string(encoded_string)

        # write to file
        args.output_file.write(encoded_string)

        path = os.path.realpath(args.output_file.name)

        # save key
        if args.save_key:
            with open(path+'.key', 'w') as key_file:
                key_file.write(conf_string)

        args.output_file.close()

        print(conf_string + '\n' + path)

    else:
        # format encoded string, if needed
        if args.groups:
            encoded_string = format_output_string(encoded_string)

        print(conf_string + '\n' + encoded_string)


if __name__ == "__main__":
    run()
