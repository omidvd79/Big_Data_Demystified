# add to list
list=[]
list.append("Big")
list.append("Data")
list.append("Demystified")
print (list)

#distinct object in a list 
txt = "Big/Data/Big/Data/Big/Data"
x = txt.split("/", 4)
list=[]
list.append(x[0])
list.append(x[1])
list.append(x[2])
list.append(x[3])

print (list)
dist_list = set(list)
print (dist_list)
