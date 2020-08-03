import datetime
from datetime import datetime
from datetime import date 

#define string data type - that contains a date
date_string= '2020-03-15'
#convert string to date - as a data type
format= '%Y-%m-%d'
date= datetime.strptime(date_string, format)

# split string to string
year, month, day = date_string.split('-')
print ("day  :" + day)
print ("month:" + month)
print ("year:" + year)

# split string to string
now = datetime.now() # current date and time
#print date after convertion to string in spesific format
print ("Now is:" +now.strftime("%Y-%M-%d"))

year = now.strftime("%Y")
print("year:", year)

month = now.strftime("%m")
print("month:", month)

day = now.strftime("%d")
print("day:", day)

time = now.strftime("%H:%M:%S")
print("time:", time)

date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
print("date and time:",date_time)
