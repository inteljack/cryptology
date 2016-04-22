'''
Data format:
     "Username" + ':' + "Encryption Mode" + "salt" + "Password"
    |---(max)---|  :  |------3 * char-----|---32---|-----96-----|

'''

import os
import sys
from getpass import getpass
# import sqlite3
from Crypto import Random
from Crypto.Cipher import AES

FILENAME = "foo.txt"
BLOCKSIZE = 16

class Account(object):
    def __init__(self, user, pwd, enopt):
        self.enopt = 'default' # default
        self.user = user
        self.pwd = pwd
        self.enopt = enopt

    def EncryptMode(self, file, login):
        with open(file, 'r') as fo:
            data = fo.readlines()
        credentials = {}
        for line in data:
            user, pwd_enopt = line.strip().split(':')
            pwd, enopt = pwd_enopt.split( )
            credentials[user] = pwd, enopt
        return credentials[login.user][1]

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

def exist_account(file, new):
    with open(file, 'r') as fo:
        data = fo.readlines()
    credentials = {}
    for line in data:
        user, pwd_enopt = line.strip().split(':')
        pwd, enopt = pwd_enopt.split( )
        credentials[user] = pwd, enopt

    if new.user in credentials:
        print "Account name already exist"
        return True
    else:
        return False

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

    if exist_account(FILENAME, new) == False:
        # Write line to the file
        line = fo.writelines(new.user+":"+new.pwd+" "+new.enopt+"\n")
        print "New account info added!!!"
    else:
        print "No account added."
# Login
elif (option == 2):
    login = Account('','','')
    login.user = raw_input("Account:\n")
    login.pwd = getpass("Password:\n")
    login.enopt = ''
    if exist_account(FILENAME, login) == True:
        login.enopt = login.EncryptMode(FILENAME, login)
        print "Encryption mode is:" + login.enopt
    else:
        print "Account not exist."



# obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
message = "The answer is no"
# print "Message in plaintext:" + message
ciphertext = obj.encrypt(message)
# print "Message in ciphertext:" + ciphertext
# '\xd6\x83\x8dd!VT\x92\xaa`A\x05\xe0\x9b\x8b\xf1'
obj2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
output = obj2.decrypt(ciphertext)
# print output


print "Operation done successfully";
# Close opend file
fo.close()
# conn.close()
