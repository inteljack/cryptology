# Cryptology
Application Security class assignment.
This application is running with command line, no UI implemented.
Featuring three chain block encryption mode `CBC, ECB and CTR` and the
encryption processes are via Python Crypto module.

Python 2.7

## Features ##
* Given a (Username, Password) pair in ASCII; store the pair to a file
* Given a (Username, Password) pair in ASCII; check if the username exists and if the password matches the one stored in a file.
* user should be able to choose ECB, CTR or CBC modes.

## Running Instructions: ##
### install python Crypto package###
`pip install pycrypto`

run code using command `python main.py`

## How does these encryption work?? ##
![CBC_dec](http://i.imgur.com/8R1sw5O.png)
![ECB_dec](http://i.imgur.com/v8A1Hoa.png)
![CTR_dec](http://i.imgur.com/uGUrdKB.png)

### Other ###
code passes PEP8 rules

* Notice data is stored into file as hex and string combined in one line.
However, when read from file, Python recognize as ASCII strings. Additional ASCII to hex conversion is implemented.


* Github URL:[inteljack](https://github.com/inteljack/cryptology)
