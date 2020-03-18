import datetime
from datetime import datetime
from datetime import date 

date_string= '2020-03-15'
format= '%Y-%m-%d'
date= datetime.strptime(date_string, format)

# curernly date is with 00:00:00
year, month, day = str(date.date()).split('-')
print ("day  :" + day)
print ("month:" + month)
print ("year:" + year)
