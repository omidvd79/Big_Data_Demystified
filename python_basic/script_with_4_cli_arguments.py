#!/usr/bin/python

import sys, getopt

usage = 'script.py --key1 val11 --key2 val --key3 val --key4 val'


def listToString(s):
    # initialize an empty string
    str1 = "|  "

    # traverse in the string
    for ele in s:
        str1 += ele+"  |  "

        # return string
    return str1

def validate_argument(opt,arg, str_array):
    if arg in str_array:
        validated_argument(arg, str_array)
    else:
        non_valid_argument(opt,arg, str_array)
    return arg

def validated_argument(arg, str_array):
    #print "User input is valid"
    return arg

def non_valid_argument(opt,arg, str_array):
    print opt+" input is NOT valid, please use one of the following: \n"
    print(listToString(str_array))
    sys.exit(1)


def parse_argv(argv):
    k1 = ''
    k2 = ''
    k2 = ''
    k4 = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["key1=", "key2=","key3=","key4="])
    except getopt.GetoptError:
        print (usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print (usage)
            sys.exit(0)
        elif opt in ("--key1"):
            str_array = ["val11", "val12", "val13"]
            k1=validate_argument(opt,arg,str_array)
        elif opt in ("--key2"):
            k2 = ["val21", "val22" ,"val23"]
            clinicalApplication =validate_argument(opt,arg,str_array)
        elif opt in ("--key3"):
            k3 = ["val31", "val32", "val33"]
            set = validate_argument(opt,arg, str_array)
        elif opt in ("--key4"):
            k4 = arg

    return k1,k2,k3,k4
def main(argv):
    k1,k2,k3,k4=parse_argv(argv)
    print (k1,k2,k3,k4)

if __name__ == "__main__":
    #print "This is the name of the script: ", sys.argv[0]
    #print "Number of arguments: ", len(sys.argv)
    #print "The arguments are: ", str(sys.argv)

    #validate 4 arguments, the first is filename_arg+ 4X(kel,val)  = 9
    if(len(sys.argv)==9):
        main(sys.argv[1:])
    else:
        print "Error in arguments, try : "+(usage)
        sys.exit(1)
