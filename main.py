'''
Data format:
     "Username" + ':' + "Encryption Mode" + "salt" + "Password"
    |---(max)---|  :  |------3 * char-----|---32---|-----96-----|

'''

import os
import sys
# import random
import datetime
from getpass import getpass
# import sqlite3
from Crypto import Random
from Crypto.Cipher import AES
from encrypt import Encryption

# FILENAME = "foo.txt"

FILENAME = "encryptdata.txt"
BLOCKSIZE = 16
# 16, 24 or 32 bytes master key. DO NOT LEAVE THIS LINE IN PRODUCTION!!!!
MASTERKEY = 'mSrtAqNBtDwHo6O8CmEIYAeGNhdaA4yX'
# must be 16 bytes long
IV = 'This is an IV456'

class Account(object):
    def __init__(self, user, pwd, enopt):
        self.enopt = 'default' # default
        self.user = user
        self.pwd = pwd
        self.enopt = enopt

    def GetAccount(self, file):
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
            print user, self.user

        if self.user in credentials:
            print "Account name found"
            return credentials[self.user]
        else:
            print "Account name not found"
            credentials[self.user] = ('', '', '')
            return credentials[self.user]

def verify(option):
    try:
        opt_value = int(option)
    except ValueError:
        print "Please enter option index only."

def verify_enopt(option):
    if option in ['ECB', 'CBC', 'CTR', '']:
        print "Encrypt option correct."
    else:
        print "Encrypt option incorrect, please retry."

# conn=sqlite3.connect('accounts.db')
# print "Database created and opened succesfully"
# Open a file in append mode
fo = open(os.path.join(sys.path[0], FILENAME), "a+")
print "Name of the file: ", fo.name

option = raw_input("Options:\n"
                    "1.Create new account\n"
                    "2.Login\n"
                    "0.Exit\n")

verify(option)
option = int(option)
print "Your option is:", option
# option = int(option)

# Create new account
if (option == 1):
    new = Account('','','')
    new.user = raw_input("Account:(No special symbols allowed)\n")
    new.pwd = getpass("Password:(First letter should not be a symbol)\n")
    new.enopt = raw_input("Encrypt option(CBC, ECB, CTR):\n")
    verify_enopt(new.enopt)

    if new.GetAccount(FILENAME) == ('', '', ''):
        # Create salt and encrypt password
        timestamp = str(datetime.datetime.now())
        salt = Random.get_random_bytes(6) + timestamp
        message = salt.encode('hex') + new.pwd.encode('hex')
        newenc = Encryption(MASTERKEY, new.enopt, IV, salt.encode('hex'))
        ciphertext = newenc.EncryptPass(message)

        # Write line to the file
        line = fo.writelines(new.user+":"+new.enopt+salt.encode('hex')+ciphertext.encode('hex')+"\n")
        print "New account info added!!!"
    else:
        print "No account added."
# Login
elif (option == 2):
    login = Account('','','')
    login.user = raw_input("Account:\n")
    login.pwd = getpass("Password:\n")
    login.enopt = ''
    cred = login.GetAccount(FILENAME)
    login.enopt = cred[0]
    print login.user
    if cred != ('', '', ''):
        rev = Encryption(MASTERKEY, login.enopt, IV, cred[1])
        hh =  rev.DecryptPass(cred[2])
        print "Your password is: " + hh

        print "Encryption mode is:" + login.enopt
    elif login.GetAccount(FILENAME) == ('', '', ''):
        print "Account not exist."
    else:
        print "Error - GetAccount() return illegal data."



print "Operation done successfully";
# Close opend file
fo.close()
# conn.close()
