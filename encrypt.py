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
password = 'password1'
username = 'Chris'

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
    salt = enopt_salt_pwd[3:35]
    pwd = enopt_salt_pwd[35:131]
    credentials[user] = (enopt, salt, pwd)

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
        # if data <= 96:

        return data

    def __unpad(self, s):
        '''
        This strips all of the 0x00 from the string passed in.

        @param s: the byte string to unpad
        @return: unpadded byte string
        '''
        s = s.rstrip(b'\x00')
        return s

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
print "salt: ", salt
print "salt(hex): ", salt.encode('hex')
print "Salt length: ", len(salt)
print "Salt type: ", type(salt)
# salt = SHA256.new(timestamp)
# print len(str(salt))
#
# new = Encryption(MASTERKEY, credentials['Danis'][1], IV)
# # print new.EncryptPass(credentials['Danis'][0])
# temp = new.EncryptPass(credentials['Danis'][0])
# # print temp.encode("hex")
# # line = fo.writelines(temp.encode("hex")+"\n")
# # line = fo.writelines("".join(hex(ord(n)) for n in temp)+"\n")


# obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
obj = AES.new(MASTERKEY, AES.MODE_CBC, IV)
# message = password
message = salt.encode('hex') + password.encode('hex')
# print concat
print "message length", len(message)
if (len(message) % BLOCKSIZE == 0):
    padmsg = message
else:
    padding_required = BLOCKSIZE - (len(message) % BLOCKSIZE)
    padChar = b'\x00'
    padmsg = message.encode('utf-8') + padding_required * padChar
    print "padmsg length", len(padmsg)

# print "Message in plaintext:" + message
ciphertext = obj.encrypt(padmsg)
line = fo.writelines(username+":"+"CBC"+salt.encode('hex')+ciphertext.encode('hex')+"\n")

# print "cipher: ", ciphertext.encode('hex'), len(ciphertext)

# print "Message in ciphertext:" + " ".join(hex(ord(n)) for n in ciphertext)
# '\xd6\x83\x8dd!VT\x92\xaa`A\x05\xe0\x9b\x8b\xf1'
obj2 = AES.new(MASTERKEY, AES.MODE_CBC, IV)
output = obj2.decrypt(ciphertext)
output = output.rstrip(b'\x00')
print output.decode('hex')[32:]
print "output message length", len(output)

# Close opend file
fo.close()
