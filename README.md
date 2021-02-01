# Enigma
|              |                      |
| ------------ | -------------------- |
| __Author:__  | Yurii Bliusiuk       |
| __Email:__   | ura.blusuk@gmail.com |
| __License:__ | MIT                  |


<br />


# Description
Emulate (replicate) functionality of the physical Enigma machine.

<br />

# Installation

    pip install yb-enigma



# Usage (cli)

    enigma [ARGS]...

## __Input__ 
|                        |                                                            |
| ---------------------- | ---------------------------------------------------------- |
| -s, --string           | String to encode                                           |
| -i, --input-file       | Path to source file                                        |
| -cnfg, --configuration | Configuration string (see __Configuration string format__) |
| -k, --key-file         | Path to file with key (Configuration string)               |

<br />

## __Output__ 
|                   |                                                                                                                |
| ----------------- | -------------------------------------------------------------------------------------------------------------- |
| -                 | Default: print key and encoded string to console                                                               |
| -o, --output-file | Path to destination file                                                                                       |
| -sk, --save-key   | Save key to file. Key will be saved to /path/to/destination_file_name.key <br /> Can only be used in FILE mode |

<br />

## __Args__ 
|                               |                                                                                                                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| -d, --debug                   | Enable debug output                                                                                                                                                      |
| -rcnfg --random-configuration | Set random rotors, reflector and plugboard configuration                                                                                                                 |
| -ks, --keep-spaces            | Keep spaces in input string                                                                                                                                              |
| -kx, --keep-special           | Keep all special characters in input string.                                                                                                                             |
| -kn, --keep-new-line          | Keep new line charecters in input string.                                                                                                                                |
| -g, --groups                  | Divide output string to groups <br />  Example: "ENIGMA IS COOL" => "ENIGM AISCO OL"  <br />   Can`t be used with '--keep-spaces', '--keep-special' or '--keep-new-line' |

<br />

## __Configuration string__
Example:

    A II:10-I:3-III:20 AB:CD

+ A - reflector
+ II:10-I:3-III:20 - rotors
  + II:10 - set first rotor to II at position 10
  + I:3 - set second rotor to I at position 3
  + III:20 - set third rotor to III at position 20
+ AB:CD - plugboard
  + AB - Plug pair A to B
  + CD - Plpug pair C to D

<br />

## __Examples__
Encode string "Hello, World!" using random configuration:  
NOTE: special characters must be escaped by "\\"

    $ enigma-cli -s "Hello, World\!" -rcnfg

Encode string "Hello, World!" using random configuration, keeping spaces and special characters:

    $ enigma-cli -s "Hello, World\!" -rcnfg -ks -kx

Encode string "Hello, World!" using random configuration, keeping spaces and special characters, output to file ./encoded.txt, key will be saved to ./encoded.key:

    $ enigma-cli -s "Hello, World\!" -rcnfg -o ./encoded.txt -sk -ks -kx

Encode text from ./text.txt using "A II:10-I:3-III:20 AB:CD" configuration:

    $ enigma-cli -f ./text.txt -cnfg "A II:10-I:3-III:20 AB:CD"

Encode text from ./text.txt using random configuration, output to file ./encoded.txt:

    $ enigma-cli -f ./text.txt -rcnfg -o ./encoded.txt

Encode text from ./text.txt using random configuration, keeping spaces, special characters and new-line charecters, output to file ./encoded.txt, key will be saved to ./encoded.key:

    $ enigma-cli -f ./text.txt -rcnfg -o ./encoded.txt -sk -ks -kx -kn

# Usage (as module)

Import:
``` python
from yb_enigma import Enigma, Rotor, Reflector, Plugboard, parse_configuration
```

Encode string:
``` python
enigma = Enigma(random_cnfg=True)                   # Create enigma instance

encoded_string = enigma.encode('Hello, World!')     # Encode "Hello, World!"
```

Encode text from file:
``` python
enigma = Enigma(random_cnfg=True)                   # Create enigma instance

encoded_string = ''
with open('./text.txt', 'r') as file:               # Open file to read
    char = file.read(1)                             # Read first byte
    while char: 
        if char.isalpha():                          # If char is [a-zA-Z]
            encoded_string += enigma.encode(char)   # Encode char and add to encoded_string
            char = file.read(1)                     # Read next byte
```

Custom configuration (manually):
``` python
reflector = Reflector.A()                           # Reflector
rotors_list = [                                     # List of rotors
    Rotor.I(pos=2), 
    Rotor.II(pos=10), 
    Rotor.III(pos=0),
]
plugboard = Plugboard(pairs=[                       # Plugboard
    {'a', 'b'},
    {'c', 'd'},
])

enigma = Enigma(                                    # Create enigma instance with
    reflector   = reflector,                        # predefined configuration
    rotors_list = rotors_list,
    plugboard   = plugboard,
)
```

Custom configuration (from Configuration string):
``` python
reflector, rotors_list, plugboard = parse_configuration("A I:2-II:10-III:0 AB:CD")

enigma = Enigma(                                    # Create enigma instance with
    reflector   = reflector,                        # predefined configuration
    rotors_list = rotors_list,
    plugboard   = plugboard,
)
```

Get/set configuration using Configuration string:
``` python
enigma = Enigma(random_cnfg=True)                   # Create enigma instance

configuration_string = enigma.get_configuration()   # Get configuration string
enigma.set_configuration(configuration_string)      # Set configuration
```

# How it works
Main parts are:
## Rotor
In real Enigma machine, rotors are discs with 26 brass, spring-loaded, electrical contact pins arranged in a circle on one face, with the other face housing 26 corresponding electrical contacts in the form of circular plates.  
Inside the body of the rotor, 26 wires connect each pin on one side to a contact on the other in a complex pattern.  
This way, we have very simple encryption algorithm (basically substitution cipher). For example, the pin corresponding to the letter E might be wired to the contact for letter T on the opposite face, and so on.  
Enigma's security comes from using several rotors in series (usually three or four) and the regular stepping movement of the rotors, thus implementing a polyalphabetic substitution cipher.  

In program this is made by each Rotor knowing it's "key": string, containing all english letter (basically it's permutation of alphabet).  
To find corresponding letter, you get letter's position in alphabet and then get letter in "key" at this position. For example, we need to find corresponding letter for "c" having key "ekmflgdqvzntowyhxuspaibrcj": position in alphabet is 3, third letter in "key" is "m". So, we have C => M.  
However, rotors are shifting, so N'th letter in alphabet corresponds to (N+Rotor.position)'th letter in "key"  

Also, important part of Enigma's encoding algorithm is the fact, that for each pressed letter (in our case encoded letter), first rotor shifts (rotates) by 1. Moreover, rotors are connected such a way, that when first rotor makes full rotation, it shifts second rotor by 1. The same thing second rotor does with third and so on.

### Example:
For simplicity, lets consider we have only 5 letters in alphabet. Our Enigma has 3 rotors with following keys:
1. "cbdae"
2. "decba"
3. "acdeb"

All rotors are at starting position (let's say posiiton 0). We want to encode string "cad". The steps are going to be:
1. press (encode) "c": 
   1. first rotor shifts, so it's position is 1 now 
   2. position of "c" in alphabet is 3
   3. (3+1)'th letter in first rotor "key" is "a"
   4. position of "a" in alphabet is 1, second rotor's position is 0
   5. (1+0)'th letter in second rotor "key" is "d"
   6. position of "d" in alphabet is 4, third rotor's position is 0
   7. (4+0)'th letter in third rotor "key" is "e"
   8. "e" is the result
2. press (encode) "a": 
   1. first rotor shifts, so it's position is 2 now 
   2. position of "a" in alphabet is 1
   3. (1+2)'th letter in first rotor "key" is "d"
   4. position of "d" in alphabet is 4, second rotor's position is 0
   5. (4+0)'th letter in second rotor "key" is "b"
   6. position of "b" in alphabet is 2, third rotor's position is 0
   7. (2+0)'th letter in third rotor "key" is "c"
   8. "c" is the result
3. press (encode) "d": 
   1. first rotor shifts, so it's position is 3 now 
   2. position of "d" in alphabet is 4
   3. (4+3)'th letter in first rotor "key" is "b" __*NOTE: actually, there is no 7'th letter, so it's (7 % 5)'th letter*__
   4. position of "b" in alphabet is 2, second rotor's position is 0
   5. (2+0)'th letter in second rotor "key" is "e"
   6. position of "e" in alphabet is 5, third rotor's position is 0
   7. (5+0)'th letter in third rotor "key" is "b"
   8. "b" is the result

__Result:__ "cad" => "ecb"

## Reflector
Previously, we have encoded string "cad" such a way, that each letter "went" from the first rotor to the second one, from the second to third and so on. However, what should actually happen, is that each letter is "going" through all rotors from the first to the last, then through the __reflector__, and back through all rotors, but now from the last to the first. 

![Enigma-action](https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Enigma-action.svg/400px-Enigma-action.svg.png)

So, __reflector__ is basically doing the same job as the rotor does, but it "encodes" and then redirects letter (electrical signal in real Enigma) back to the last rotor and __it's not moving__ during work.  
__IMPORTANT:__ in reflector's "key", letters are pointing on each other in pairs, e.g. if "a" is pointing to "c", "c" must be pointing to "a"

## Plugboard
The plugboard permitted variable wiring that could be reconfigured by the operator.  

A cable placed onto the plugboard connected letters in pairs; for example, E and Q might be the pair. The effect was to swap those letters before and after the main rotor unit. For example, when an operator pressed E, the signal was diverted to Q before entering the rotors.

<img src="https://upload.wikimedia.org/wikipedia/commons/2/27/Enigma-plugboard.jpg" width="500">

<br /><br />

# Implementation

All the steps are well described in the comments. Small summary:

## Rotor
To implement rotors rotation system (each rotor rotates the next one after it's full rotation, more in "How it works -> Rotor"), rotors are organised using Doubly linked list.  
Also, to optimise encoding, I am creating *coding_list* - list of each key letter's num in alphabet (e.g. "ecabd" => [4, 2, 0, 1, 3]).  
Each rotor has it's number: I, II, ..., VIII and position (rotation step).

## Reflector
As previously said in "How it works -> Reflector", reflector is doing pretty much the same work as Rotor do, but 
1) it is not moving during encoding, so it doesn't have position.
2) it doesn't have reverse mode while getting corresponding letter.

## Plugboard
Plugpairs are stored using *set* data type (it just feels more ideologically correct for me, however in terms of speed, it is just the same as *list* or *tuple*, because of small amount of data stored (it's always only two strings of length 1)).  
Pairs are stored in *list*.  

During encoding, it returns corresponding char or char itself, if it's not in plugged pairs

## Enigma
Finally an Enigma class.  

Can be initialised using random or default configuration.  
Takes care of creating doubly linked list of rotors.

While encoding, shift the first rotor and passes letter through the whole chain (plugboard -> rotors -> reflector -> rotors (desc) -> plugboard).

## CLI
The CLI script is pretty simple script, which parses passed arguments, and works based on those argument. 

There are basically 2 modes: string and file. In the string mode, input is passed as string using (-s \<STRING\>, --string \<STRING\>) argument. In the file mode, input is passed using file, path is set by (-i \<PATH\>, --input-file \<PATH\>).
