# this will sha256 a string
from hashlib import sha256
output = sha256("BigDataDemsytified".encode('utf-8'))
print(output.hexdigest())
