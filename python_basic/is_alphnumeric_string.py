a_string = 'BigDataDemystified2020!@#$%'

isalnum = a_string.isalnum()

print('Is String Alphanumeric :', isalnum)

alphanumeric_filter = filter(str.isalnum, a_string)
alphanumeric_string = "".join(alphanumeric_filter)
print(alphanumeric_string)
