import os
import sys
from Crypto.Cipher import AES

# Open a file in witre mode
fo = open(os.path.join(sys.path[0],"foo.txt"), "rw+")
print "Name of the file: ", fo.name

# Assuming file has following 5 lines
# This is 1st line
# This is 2nd line
# This is 3rd line
# This is 4th line
# This is 5th line

seq = ["This is 6th line\n", "This is 7th line"]
# Write sequence of lines at the end of the file.
fo.seek(0, 2)
line = fo.writelines( seq )

# Now read complete file from beginning.
fo.seek(0,0)
for index in range(7 ):
   line = fo.next()
   print "Line No %d - %s" % (index, line)

# Close opend file
fo.close()


obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
message = "The answer is no"
print "Message in plaintext:" + message
ciphertext = obj.encrypt(message)
print "Message in ciphertext:" + ciphertext
# '\xd6\x83\x8dd!VT\x92\xaa`A\x05\xe0\x9b\x8b\xf1'
obj2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
print obj2.decrypt(ciphertext)
# 'The answer is no'
