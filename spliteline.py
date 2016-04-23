"""
@Editor:Ying-Ta Lin
"""
credentials = {}
with open('foo.txt', 'r') as f:
    data = f.readlines()
    #print data

for line in data:
    user, pwd = line.strip().split(':')
    pwd, enopt = pwd.split( )
    credentials[user] = pwd

print credentials['Danis']
print credentials
