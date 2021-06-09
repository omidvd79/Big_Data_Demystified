#!/usr/bin/env python
import sys

#get filename  from enduser  
filename='test5.csv' #init value
#print(str(sys.argv[1])) #argv[0] is filename
filename=str(sys.argv[1])
file = open(filename, "rb")

byte = file.read(1)
my_str=''

while byte:
#byte=false at end of file
	if byte!=b'\xff' and byte!=b'\x01':
		#print(byte)
		my_str+=byte.decode("utf-8") 
	elif byte==b'\xff':
		my_str+="|" #adding seperator instead of bad byte
	elif byte==b'\x01':	# is a wierd seprator
		my_str+=","
	byte = file.read(1)
#print(my_str)

with open(filename+"_parsed", 'w') as f:
    f.write(my_str.replace("000000","").replace("\\N",""))
