'''
Data format:
     "Username" + ':' + "Encryption Mode" + "salt" + "Password"
    |---(max)---|  :  |------3 * char-----|---32---|-----96-----|

'''
import os
import sys
import random
import datetime
from Crypto import Random
from Crypto.Cipher import AES

'''
For testing parameters
'''
password = 'password'
username = 'David'

'''
end
'''

FILENAME = "encryptdata.txt"
BLOCKSIZE = 16
# 16, 24 or 32 bytes master key. DO NOT LEAVE THIS LINE IN PRODUCTION!!!!
MASTERKEY = 'mSrtAqNBtDwHo6O8CmEIYAeGNhdaA4yX'
# must be 16 bytes long
IV = 'This is an IV456'

with open(FILENAME, 'r') as fo:
    data = fo.readlines()
credentials = {}
for line in data:
    user, enopt_salt_pwd = line.strip().split(':')
    enopt = enopt_salt_pwd[:3]
    salt = enopt_salt_pwd[3:67]
    pwd = enopt_salt_pwd[67:]
    # print len(pwd)
    credentials[user] = (enopt, salt, pwd)

fo = open(os.path.join(sys.path[0], FILENAME), "a+")
# print "Name of the file: ", fo.name

class Encryption(object):
    def __init__(self, key, enopt, iv, salt):
        self.key = key
        self.enopt = enopt
        self.iv = iv
        self.salt = salt

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
        padmsg = raw.encode('utf-8') + padding_required * padChar
        # if data <= 96:
        return padmsg

    def __unpad(self, s):
        '''
        This strips all of the 0x00 from the string passed in.
        @param s: the byte string to unpad
        @return: unpadded byte string
        '''
        s = s.rstrip(b'\x00')
        return s

    def __decode(self, cipher):
        hex_cipher = ""
        for x in cipher:
            num = ord(x)
            if num > 96:
                num = num - 87
            elif num < 58:
                num = num - 48
            else:
                print "error"
            hex_cipher += hex(num)[2:]
        return hex_cipher

    def TransMode(self):
        if self.enopt == 'ECB':
            return 1    # AES.MODE_ECB = 1
        elif self.enopt == 'CBC':
            return 2    # AES.MODE_CBC = 2
        elif self.enopt == 'CTR':
            return 6    # AES.MODE_CTR = 6
        else:   # default
            return 1    # AES.MODE_ECB = 1

    def EncryptPass(self, plaintext):
        obj = AES.new(self.key, self.TransMode(),self.iv)
        padpass = self.__pad(plaintext)
        # print " ".join(hex(ord(n)) for n in padpass)
        # print " ".join(hex(ord(n)) for n in plaintext)
        return obj.encrypt(padpass)

    def DecryptPass(self, cipher):
        obj = AES.new(self.key, self.TransMode(), self.iv)
        hex_cipher = self.__decode(cipher)
        # print "hex_cipher: ", hex_cipher
        padpass = obj.decrypt(hex_cipher.decode('hex'))
        print "padpass: ", padpass
        plaintext = self.__unpad(padpass)
        plainpwd = plaintext[64:].decode('hex')
        return plainpwd

# # print out account informations in the file
# for x in credentials:
#     print x, credentials[x]

# cred = {'John':('pass', 'ECB'), 'Dave':('p@ss', 'CTR')}
# print cred
# print cred['John'][1]
# print ("\n".join(cred))

timestamp = str(datetime.datetime.now())
# print len(timestamp)

salt = Random.get_random_bytes(6) + timestamp
# print "salt: ", salt
# print "salt(hex): ", salt.encode('hex')
# print "Salt length: ", len(salt)
# print "Salt type: ", type(salt)

# obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
# obj = AES.new(MASTERKEY, AES.MODE_CBC, IV)
# message = password
message = salt.encode('hex') + password.encode('hex')
new = Encryption(MASTERKEY, 'CBC', IV, salt.encode('hex'))
ciphertext = new.EncryptPass(message)

# line = fo.writelines(username+":"+"CBC"+salt.encode('hex')+ciphertext.encode('hex')+"\n")
print "Chris"
print "Mode: ", credentials[username][0]
print "Salt: ", credentials[username][1]
print "Cipher: ", credentials[username][2]
# intform = int(credentials['Chris'][2], 16)
rev = Encryption(MASTERKEY, credentials[username][0], IV, credentials[username][1])
hh =  credentials[username][2]
print rev.DecryptPass(hh)


# Close opend file
fo.close()
