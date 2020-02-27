#!/usr/bin/python

import sys, getopt

def main(argv):
   startDate = ''
   endDate = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["start=","end="])
   except getopt.GetoptError:
      print ('example_python_command_line_arguments.py -s <startDate> -e <endDate>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('example_python_command_line_arguments.py -s <startDate> -e <endDate>')
         sys.exit()
      elif opt in ("-s", "--start"):
         startDate = arg
      elif opt in ("-e", "--end"):
         endDate = arg
   print ('start date is ', startDate)
   print ('end   date is ', endDate)

if __name__ == "__main__":
   main(sys.argv[1:])
