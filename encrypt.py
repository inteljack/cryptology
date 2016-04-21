import os
import sys
from Crypto import Random
from Crypto.Cipher import AES

FILENAME = "foo.txt"
BLOCKSIZE = 16

with open(FILENAME, 'r') as fo:
    data = fo.readlines()
credentials = {}
for line in data:
    user, pwd_enopt = line.strip().split(':')
    pwd, enopt = pwd_enopt.split( )
    credentials[user] = (pwd, enopt)

fo = open(os.path.join(sys.path[0], FILENAME), "a+")
# print "Name of the file: ", fo.name

class Encryption(object):
    def __init__(self, key, enopt, iv):
        self.key = key
        self.enopt = enopt
        self.iv = iv

    def __pad(self, raw):
        '''
        This right pads the raw text with 0x00 to force the text to be a
        multiple of 16.  This is how the CFX_ENCRYPT_AES tag does the padding.

        @param raw: String of clear text to pad
        @return: byte string of clear text with padding
        '''
        if (len(raw) % BLOCKSIZE == 0):
            return raw
        padding_required = BLOCKSIZE - (len(raw) % BLOCKSIZE)
        padChar = b'\x00'
        data = raw.encode('utf-8') + padding_required * padChar
        return data

    def TransMode(self):
        # AES.MODE_ECB = 1
        # AES.MODE_CBC = 2
        # AES.MODE_CTR = 6
        if self.enopt == 'ECB':
            return 1
        elif self.enopt == 'CBC':
            return 2
        elif self.enopt == 'CTR':
            return 6
        else: # default
            return 1

    def EncryptPass(self, plaintext):
        obj = AES.new(self.key, self.TransMode(),self.iv)
        padpass = self.__pad(plaintext)
        # print " ".join(hex(ord(n)) for n in padpass)
        # print " ".join(hex(ord(n)) for n in plaintext)
        return obj.encrypt(padpass)

# # print out account informations in the file
# for x in credentials:
#     print x, credentials[x]

# cred = {'John':('pass', 'ECB'), 'Dave':('p@ss', 'CTR')}
# print cred
# print cred['John'][1]
# print ("\n".join(cred))

new = Encryption('This is a key123', credentials['Danis'][1], 'This is an IV456')
# print new.EncryptPass(credentials['Danis'][0])
temp = new.EncryptPass(credentials['Danis'][0])
# print temp.encode("hex")
line = fo.writelines(temp.encode("hex")+"\n")
# line = fo.writelines("".join(hex(ord(n)) for n in temp)+"\n")



# obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
message = "The answer is no"
# print "Message in plaintext:" + message
ciphertext = obj.encrypt(message)
# print "Message in ciphertext:" + " ".join(hex(ord(n)) for n in ciphertext)
# '\xd6\x83\x8dd!VT\x92\xaa`A\x05\xe0\x9b\x8b\xf1'
obj2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
output = obj2.decrypt(ciphertext)
# print output

# Close opend file
fo.close()
