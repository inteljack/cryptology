import os
import sys
# import sqlite3
from Crypto.Cipher import AES

class Account(object):
    def __init__(self, user, pwd, enopt):
        self.user = user
        self.pwd = pwd
        self.enopt = enopt

def verify(option):
    try:
        opt_value = int(option)
    except ValueError:
        print "Please enter option index only."

def verify_enopt(option):
    if option in ['ECB', 'CBC', 'CTR']:
        print "Encrypt option correct."
    else:
        print "Encrypt option incorrect, please retry."

# conn=sqlite3.connect('accounts.db')
# print "Database created and opened succesfully"
# Open a file in append mode
fo = open(os.path.join(sys.path[0], "foo.txt"), "a+")
print "Name of the file: ", fo.name

option = raw_input("Options:\n"
                    "1.Create new account and pass.\n"
                    "2.Find Account\n"
                    "0.Exit\n")

verify(option)
option = int(option)
print "Your option is:", option
# option = int(option)

if (option == 1):
    new = Account('','','')
    new.user = raw_input("Account:(No special symbols allowed)\n")
    new.pwd = raw_input("Password:(First letter should not be a symbol)\n")
    new.enopt = raw_input("Encrypt option(CBC, ECB, CTR):\n")
    verify_enopt(new.enopt)


# seq = ["This is 6th line\n", "This is 7th line"]
# Write sequence of lines at the end of the file.
# fo.seek(0, 2)


# Now read complete file from beginning.
# fo.seek(0, 0)
# for index in range(7):
#     line = fo.next()
#     print "Line No %d - %s" % (index, line)

# obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
message = "The answer is no"
print "Message in plaintext:" + message
ciphertext = obj.encrypt(message)
print "Message in ciphertext:" + ciphertext
# '\xd6\x83\x8dd!VT\x92\xaa`A\x05\xe0\x9b\x8b\xf1'
obj2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
output = obj2.decrypt(ciphertext)
print output
# 'The answer is no'

# line = fo.writelines("Message in plaintext:" + message + "\n")
# line = fo.writelines("Message in ciphertext:" + ciphertext + "\n")
# line = fo.writelines(output)


print "Operation done successfully";
# Close opend file
fo.close()
# conn.close()
