'''
@@Author: Ying-Ta Lin
Data format:
     "Username" + ':' + "Encryption Mode" + "salt" + "Password"
    |---(max)---|  :  |------3 * char-----|---32---|-----96-----|

'''
import os
import sys
import datetime
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util import Counter

FILENAME = "encryptdata.txt"
BLOCKSIZE = 16
NUM_COUNTER_BITS = 128
# 16, 24 or 32 bytes master key. DO NOT LEAVE THIS LINE IN PRODUCTION!!!!
MASTERKEY = 'mSrtAqNBtDwHo6O8CmEIYAeGNhdaA4yX'
# must be 16 bytes long
IV = 'This is an IV456'


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
        if self.enopt == 'CTR':
            counter = Counter.new(NUM_COUNTER_BITS)
            obj = AES.new(self.key, self.TransMode(), self.iv, counter=counter)
        else:
            obj = AES.new(self.key, self.TransMode(), self.iv)
        padpass = self.__pad(plaintext)
        return obj.encrypt(padpass)

    def DecryptPass(self, cipher):
        if self.enopt == 'CTR':
            counter = Counter.new(NUM_COUNTER_BITS)
            obj = AES.new(self.key, self.TransMode(), self.iv, counter=counter)
        else:
            obj = AES.new(self.key, self.TransMode(), self.iv)
        hex_cipher = self.__decode(cipher)
        padpass = obj.decrypt(hex_cipher.decode('hex'))
        plaintext = self.__unpad(padpass)
        plainpwd = plaintext[64:].decode('hex')
        return plainpwd
