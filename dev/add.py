"""
@Editor:Ying-Ta Lin
"""

import os
import sys
# import sqlite3
from Crypto.Cipher import AES

with open('foo.txt', 'r') as fo:
    data = fo.readlines()
fo = open(os.path.join(sys.path[0], "foo.txt"), "a+")

new_user = raw_input("Account:(No special symbols allowed)\n")
new_pwd = raw_input("Password:(First charactor should not be symbol)\n")
new_enopt = raw_input("Encrypt option(CBC, ECB, CTR):\n")

# Check if there is a existing account name
credentials = {}
for line in data:
    user, pwd_enopt = line.strip().split(':')
    pwd, enopt = pwd_enopt.split( )
    credentials[user] = pwd

if new_user in credentials:
    print "exist"
else:
    # Write line to the file
    line = fo.writelines(new_user+":"+new_pwd+" "+new_enopt+"\n")
    print "New Account info added!!!"

obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
message = "The answer is no"
print "Message in plaintext:" + message
ciphertext = obj.encrypt(message)
print "Message in ciphertext:" + ciphertext
# '\xd6\x83\x8dd!VT\x92\xaa`A\x05\xe0\x9b\x8b\xf1'
obj2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
output = obj2.decrypt(ciphertext)
print output

print "Operation done successfully";
# Close opend file
fo.close()
