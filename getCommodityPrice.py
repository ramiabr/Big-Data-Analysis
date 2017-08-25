#!/usr/bin/python
import sys, getopt
import os
import re
import sys

def printf(format, *args):
    sys.stdout.write(format % args)
   
try:
  import MySQLdb
except:
  print "ERROR: \"MySQLdb\" module is not installed, please install and try again"
  sys.exit(0)

## Initializating Database
global db
global cur
global date 
date = {}


def openDB():
  global db
  global cur
  
  db = MySQLdb.connect(host="localhost",  # your host 
     user="root",	   # username
     passwd="scu@123",     # password
     db="goldSilverPrices")   # name of the database
 
  # Create a Cursor object to execute queries.
  cur = db.cursor()

def closeDB():
  global db
  global cur

  db.close()


def main():  
  parse_options()
  dataAnalytics()

def dataAnalytics():
  global date
  global cur
  prices_array = []
  mean = float(0)
  var  = float(0)
  n    = int(0)
  debug_str = ""
  
  try:
    openDB()
  except:
    print "ERROR: Couldn't open Database, hence exiting"
    sys.exit(0)

  query = "SELECT * from " + date["dtype"] + " WHERE date >= '" + date["start"] + "\' AND date <= \'" + date["end"] + "\';"
  cur.execute(query)
  result = cur.fetchall()
  
  if (len(result) == 0):
    print "\n\nERROR: Selected Dates did not yield any results, Try again with other Range !!"
    sys.exit(0)
  
  ## Calculate mean  
  for item in result:
    price = re.sub(',', '', item[1]) 
    prices_array.append(price)
    mean = mean + float(price)
    n = n + 1
  mean  = float(mean/n)
   
  ## Calculate Variance 
  for pr in prices_array:
    tmp = float(pr) - mean
    tmp = tmp * tmp
    var = var + tmp   
    debug_str =  str(pr) + ";" + str(debug_str) 
  
  var  = float(var/(n-1))
  
  printf("%s %.2f %.2f \n", date["dtype"] , mean, var)
   
  closeDB()

  #print "[" , debug_str , "]" 
  #print "Mean: ", float(mean)
  #print "Var : ", float(var/(n-1))


def sanityCheckDate(pattern, inp):
  year  = pattern.group(1)
  month = pattern.group(2)
  day	= pattern.group(3)
  
  if(re.search('^\d$', month)):
    month = "0" + month

  if(re.search('^\d$', day)):
    day = "0" + day 
  
  if(int(month) > 12):
    print "ERROR: Month Can't be > 12, ", month, "(", inp , ")"
    usage() 
  
  if(int(day) > 31):
    print "ERROR: Day can't be > 31, ", day , "(" , inp , ")"
    usage()
    
  return(year, month, day)

def parse_options():     
  global date 
  
  ## Exit if not sufficient arguments given
  if(len(sys.argv) != 4):
     print "ERROR: Expected 3 arguments, but given ", len(sys.argv)
     usage()
    
  ## Ensure Inputs are in acceptable format
  pattern = re.search('(\d\d\d\d)-(\d+)-(\d+)', sys.argv[1], re.IGNORECASE)
  if(pattern):
    year, month, day = sanityCheckDate(pattern, sys.argv[1])
    date["start"] =  year + "-" + month + "-" + day 
    #print date["start"], "\n"
  else:
    print "ERROR: Expected Start Date format \"YYYY-MM-DD\" but given with ", sys.argv[1]
    usage()
  

  ## Ensure Inputs are in acceptable format
  pattern = re.search('(\d\d\d\d)-(\d+)-(\d+)', sys.argv[2], re.IGNORECASE)
  if(pattern):
    year, month, day = sanityCheckDate(pattern, sys.argv[2])
    date["end"] =  year + "-" + month + "-" + day 
    #print date["end"], "\n"
  else:
    print "ERROR: Expected End Date format \"YYYY-MM-DD\" but given with ", sys.argv[2]
    usage()
  
  ##  
  inpText = str.lower(sys.argv[3])
  if(inpText == "gold" or inpText == "silver"):
    date["dtype"] = inpText 
  else:
    print "ERROR: Expected \"gold\" (or) \"silver\" keyword but given with, \"", sys.argv[3], "\""
    usage()
  
  print "\nINFO: Performing Data Analysis "
  print "Start Date: ", date["start"] ,", End Date: ", date["end"], ", Analysis Type: ", date["dtype"]


## Print Usage information to user and exit 
def usage(): 
    print "\nUsage: " , sys.argv[0] , " <Start Date>  <End Date> <Commodity Name>"
    print "--------------------------------------------------------------"
    print "Start Date in format - YYYY-MM-DD  "
    print "End Date in format   - YYYY-MM-DD  "
    print "Commodity name       - gold|silver "
    print "Output:"
    print "gold  : Mean , Variance   (or)"
    print "silver:  Mean , Variance  "
    print "" 
    sys.exit(2)

if __name__ == "__main__":
    main()  
