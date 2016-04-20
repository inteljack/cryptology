import os
import sys
# import sqlite3
from Crypto.Cipher import AES

FILENAME = "foo.txt"

class Account(object):
    def __init__(self, user, pwd, enopt):
        self.enopt = 'default' # default
        self.user = user
        self.pwd = pwd
        self.enopt = enopt

    def EncryptMode(self,file, exist_user):
        with open(file, 'r') as fo:
            data = fo.readlines()
        credentials = {}
        for line in data:
            user, pwd_enopt = line.strip().split(':')
            pwd, enopt = pwd_enopt.split( )
            credentials[user] = enopt
        return credentials[exist_user]

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

def exist_account(file, new_user):
    with open(file, 'r') as fo:
        data = fo.readlines()
    credentials = {}
    for line in data:
        user, pwd_enopt = line.strip().split(':')
        pwd, enopt = pwd_enopt.split( )
        credentials[user] = pwd

    if new_user in credentials:
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
    new.pwd = raw_input("Password:(First letter should not be a symbol)\n")
    new.enopt = raw_input("Encrypt option(CBC, ECB, CTR):\n")
    verify_enopt(new.enopt)

    if exist_account(FILENAME, new.user) == False:
        # Write line to the file
        line = fo.writelines(new.user+":"+new.pwd+" "+new.enopt+"\n")
        print "New Account info added!!!"

# Login
elif (option == 2):
    login = Account('','','')
    login.user = raw_input("Account:\n")
    login.pwd = raw_input("Password:\n")
    login.enopt = ''
    if exist_account(FILENAME, login.user) == True:
        login.enopt = login.EncryptMode(FILENAME, login.user)
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
