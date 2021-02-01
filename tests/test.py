import unittest
from yb_enigma import Enigma, Rotor, Reflector, Plugboard
from yb_enigma import InvalidConfigurationString, InvalidPlugboardPair, NotUniquePair
from yb_enigma import parse_configuration, ALPH
# import utils


class TestRotors(unittest.TestCase):

    def test_keys(self):
        for rotor in Rotor.list():
            with self.subTest(i=rotor.num):
                self.assertEqual(sorted(rotor.coding_list), list(range(26)))

    def test_encoding(self):
        for rotor in Rotor.list():
            for char in ALPH:
                with self.subTest(i=rotor.num):
                    encoded_char = rotor.encode(char)
                    decoded_char = rotor.encode(encoded_char, reverse=True)
                    self.assertEqual(char, decoded_char)


class TestPlugboard(unittest.TestCase):

    def test_random_full(self):
        plugboard = Plugboard()
        for _ in range(13):
            plugboard.plug_random()

        self.assertEqual(len(plugboard.pairs), 13)

    def test_random_more(self):
        plugboard = Plugboard()
        for _ in range(26):
            plugboard.plug_random()

        self.assertEqual(len(plugboard.pairs), 13)

    def test_errors(self):
        plugboard = Plugboard(pairs=[{'a', 'b'}])

        cases = [
            ({'c', 'c'}, InvalidPlugboardPair),
            ({'b', 'c'}, NotUniquePair),
        ]

        for case in cases:
            pair, exception = case
            with self.subTest(i=pair):
                self.assertRaises(exception, plugboard.plug, pair)


class TestEnigmaEncryption(unittest.TestCase):

    def test_encrypt(self):
        enigma = Enigma()

        for i in range(len(Rotor.list())):
            for j in range(len(Rotor.list())):
                for l in range(len(Rotor.list())):
                    for k in range(len(Reflector.list())):
                        rotor1 = Rotor.list()[i]
                        rotor2 = Rotor.list()[j]
                        rotor3 = Rotor.list()[l]
                        reflector = Reflector.list()[k]
                        conf_str = reflector.num+' '+rotor1.num+'-'+rotor2.num+'-'+rotor3.num
                        with self.subTest(i=conf_str):
                            enigma.set_configuration(conf_str)
                            conf = enigma.get_configuration()
                            enc = enigma.encode('abcdefghijklmnopqrstuvwxyz')
                            enigma.set_configuration(conf)
                            dec = enigma.encode(enc)
                            self.assertEqual('abcdefghijklmnopqrstuvwxyz', dec)


class TestConfStringParse(unittest.TestCase):

    def test_parse(self):
        cases = {
            "A II:1-I:3-III:20 AB:CD:XZ:GE": [
                'A', 'II:1-I:3-III:20', [{'a', 'b'}, {'c', 'd'}, {'x', 'z'}, {'g', 'e'}]
            ],
            "A II:1-I:3-III:20": [
                'A', 'II:1-I:3-III:20', []
            ],
            "B II:1-I:3": [
                'B', 'II:1-I:3', []
            ],
            "B I-II": [
                'B', 'I:0-II:0', []
            ],
            "B I-II AB": [
                'B', 'I:0-II:0', [{'a', 'b'}]
            ]
        }

        for string, result in cases.items():
            with self.subTest(i=string):
                reflector, rotors_list, plugboard = parse_configuration(string)
                # print(string, reflector, '-'.join([str(rotor) for rotor in rotors_list]), plugboard)
                self.assertEqual(result[0], str(reflector))
                self.assertEqual(result[1], '-'.join([str(rotor) for rotor in rotors_list]))
                self.assertEqual(result[2], plugboard.pairs)

    def test_parse_conf_invalid_string(self):
        cases = {
            "": InvalidConfigurationString,
            "A": InvalidConfigurationString,
            "Z": InvalidConfigurationString,
            "A abc": InvalidConfigurationString,
            "A B C D": InvalidConfigurationString,
            "abcde": InvalidConfigurationString,
            "A I-II-III ABC:ER": InvalidConfigurationString,
            "A I-II AA": InvalidPlugboardPair,
            "A I-II AB:AD": NotUniquePair,
        }

        for string, exception in cases.items():
            with self.subTest(i=string):
                self.assertRaises(exception, parse_configuration, string)


if __name__ == '__main__':
    unittest.main()
