#!/usr/bin/python
#
# Description:  - This program will read My SQL Database for gold and silver tables
#		- Compute Mean (x1 + x2 + x3 +  ... + xn)/n 
#		- Variance (1/(n-1)) * ( (x1-M)^2 + (x2-M)^2 + ..... + (Xn-M)^2 )
#		- Print the output <Metal type> <Mean> <Variance>
#
# Inputs     :  <Start Date> <End Date> <Metal Type>
# Outputs    :  <Metal Type> <Mean> <Variance>
# 
# Dependancies:  This code requires below modules to be installed and available
#		 - MySQLdb
#		 - Python 2.7
#
# Note: This code has been tested in Python 2.7

import sys, getopt
import os
import re
import sys
from datetime import datetime

## Print module to display formatted result
def printf(format, *args):
    sys.stdout.write(format % args)

# Import MySQLdb 
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

## Open Database 
def openDB():
  global db
  global cur

  try:
    db = MySQLdb.connect(host="localhost",  # your host 
       user="root",	   # username
       passwd="scu@123",     # password
       db="goldSilverPrices")   # name of the database
  except:
    print "ERROR: Unable to open MySQLdb \"goldSilverPrices\" "
    sys.exit(0)
 
  # Create a Cursor object to execute queries.
  cur = db.cursor()

# Close db
def closeDB():
  global db
  global cur

  db.close()


############################################
##### Main Function ########################
############################################
def main():  
  # Parse Input options
  parse_options()
  
  # Data Analytics on DB
  dataAnalytics()

############################################################
## Description  : Read Database, Compute Mean, Variance		  
## Input	: Start Date, End Date, Metal Type
## Output	: Mean and Variance
############################################################
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
    s_year, s_month, s_day = sanityCheckDate(pattern, sys.argv[1])
    date["start"] =  s_year + "-" + s_month + "-" + s_day 
  else:
    print "ERROR: Expected Start Date format \"YYYY-MM-DD\" but given with ", sys.argv[1]
    usage()
  

  ## Ensure Inputs are in acceptable format
  pattern = re.search('(\d\d\d\d)-(\d+)-(\d+)', sys.argv[2], re.IGNORECASE)
  if(pattern):
    e_year, e_month, e_day = sanityCheckDate(pattern, sys.argv[2])
    date["end"] =  e_year + "-" + e_month + "-" + e_day 
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
  
  ## Make sure Start Time is lesser than End Time
  diff = datetime(int(e_year), int(e_month), int(e_day)) < datetime(int(s_year), int(s_month), int(s_day))
  
  if diff:
    print "ERROR: End Date Should be > Start Date \n\nStart Date: ", date["start"] , ", End Date: ", date["end"]
    sys.exit(0)
  
  #print "\nINFO: Performing Data Analysis "
  #print "Start Date: ", date["start"] ,", End Date: ", date["end"], ", Analysis Type: ", date["dtype"]
  
  


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
