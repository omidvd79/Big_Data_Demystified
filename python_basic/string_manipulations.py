# end with
str = "this Big Data Demystified Meetup... is wow!!!";
suffix = "wow!!!";
print str.endswith(suffix)

#contains
str = "Big Data" 
if "Data" in str:
   print ("True")
   
#string occurnaces:
str ="Does Big Data acctuall mean Data Demystified?"
#finding occurrences of 'Data'
#in complete string
print(str.count("Data"))

#string split, and get first object in the list
txt = "welcome/to/Big/Data/Demystified"
x = txt.split("/", 1)
print(x[0])


