                                               
from os import listdir
from os.path import isfile, join
mypath='/tmp/imedis/'
def iterate_folder(mypath):
        #print ("in path: "+mypath)
        onlyFiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        onlyFolders = [f for f in listdir(mypath) if not isfile(join(mypath, f))]
                
        for folder in onlyFolders:
                #print join(mypath,folder)
                itterate_folder(join(mypath,folder))
        for file in onlyFiles:
                print join(mypath,file)
iterate_folder(mypath)
