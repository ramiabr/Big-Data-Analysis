#!/usr/bin/python
#
# Description:  - This program Extracts Gold and Silver Prices from investing.com website 
#		- As First Step the program builds MySQL database "goldSilverPrices" 
#		- MySQL database will have two tables gold and silver which will store 
#		  corresponding Price Data from website 
#		- The website will be parsed using Xpath module
#		- Parsed information is updated into database 
#
# Inputs     :  None
# Outputs    :  MySQL database "goldSilverPrices" tables gold and silver
# 
# Dependancies:  This code requires below modules to be installed and available
#		 - MySQLdb
#		 - lxml
#		 - requests
#		 - Python 2.7
#
# Note: This code has been tested in Python 2.7


import sys, getopt
import os
import re

## Import MySQLdb
try:
  import MySQLdb
except:
  print "ERROR: \"MySQLdb\" module is not installed, please install and try again"
  sys.exit(0)

## Importing Xpath for HTML Parsing 
try:
  from lxml import html
  import lxml.html as LH
except:
  print "ERROR: \"lxml\" package is not installed, Please install and try again (For Python 3: sudo apt-get install python3-lxml) \n "
  sys.exit(0)

## Importing Requests module to access websites
try:
  import requests
except:
  print "ERROR: \"requests\" package is not installed, Please install and try again (pip install requests) \n "
  sys.exit(0)
  

## Global Variables
global debug 
global gold_address   
global silver_address 
global self_obj 
global db
global cur

# Global Var initialization
debug = 0
self_obj = {}

self_obj["gold", "web"]    = "https://www.investing.com/commodities/gold-historical-data"
self_obj["gold", "date"]   = "//div[@id=\"results_box\"]/table[@id=\"curr_table\"]/tbody/tr/td[1]/text()"
self_obj["gold", "price"]  = "//div[@id=\"results_box\"]/table[@id=\"curr_table\"]/tbody/tr/td[2]/text()"

self_obj["silver", "web"]   = "https://www.investing.com/commodities/silver-historical-data"
self_obj["silver", "date"]  = "//div[@id=\"results_box\"]/table[@id=\"curr_table\"]/tbody/tr/td[1]/text()"
self_obj["silver", "price"] = "//div[@id=\"results_box\"]/table[@id=\"curr_table\"]/tbody/tr/td[2]/text()"


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
    print "ERROR: Couldn't connect to MySQLdb \"goldSilverPrices\", Flow terminating"
    sys.exit(0)
  
  # Create a Cursor object to execute queries.
  cur = db.cursor()

## Delete Database
def deleteDataDB():
  global db
  global cur

  openDB()

  ## Wipe table clean
  
  #query = "TRUNCATE TABLE gold"
  try:
    query = "drop table if exists gold"
    cur.execute(query)
    
    query = "drop table if exists silver"
    cur.execute(query)
  
    ## 
    query = "CREATE TABLE gold(date DATE, price VARCHAR(20))"
    cur.execute(query)
  
    ## 
    query = "CREATE TABLE silver(date DATE, price VARCHAR(20))"
    cur.execute(query)
  except:
    print "ERROR: Couldn't "

  db.commit()  
  closeDB()

## Close database
def closeDB():
  global db
  global cur

  db.commit()
  db.close()

############################################
##### Main Function ########################
############################################
def main():  
  ## Parse Options
  parse_options()
  
  #Delete All Tables in Database
  deleteDataDB()
  
  # Open a new to build tables
  openDB()
  
  # Parse Website Gold website
  parse_websites("gold")
  
  # Parse Website
  parse_websites("silver")
  
  # Close database object 
  closeDB()
  
  # Exit Gracefully 
  print "\n\nINFO: Flow completed successfully !!"


############################################################
## Description  : Transforms date format from website format 
#		  to MySQL format
## Input	: Date from website
## Output	: Returns Date in MySQL format
############################################################
def format_date(date):
  date = re.sub(',','', date)
  month, day, year = re.split('\s+',date)
  
  if(month == "Jan"):
    month_no = "01"
  elif(month  == "Feb"):
    month_no = "02"
  elif(month  == "Mar"):
    month_no = "03"
  elif(month  == "Apr"):
    month_no = "04"
  elif(month  == "May"):
    month_no = "05"
  elif(month  == "Jun"):
    month_no = "06"
  elif(month  == "Jul"):
    month_no = "07"
  elif(month  == "Aug"):
    month_no = "08"
  elif(month  == "Sep"):
    month_no = "09"
  elif(month  == "Oct"):
    month_no = "10"
  elif(month  == "Nov"):
    month_no = "11"
  elif(month  == "Dec"):
    month_no = "12"
  else:
    month_no = "00"

  return(year + "-" + month_no + "-" + day)  

############################################################
## Description  : Parse websites and extracts Gold/Silver 
##		  Prices
## Input	: Specify gold (or) silver
## Output	: Builds Database with Price history 
##		  Information
############################################################
def parse_websites(tableName):  
  global debug
  
  web = self_obj[tableName, "web"] 

  print "INFO: Parsing HTML : ", web

  dateXpath   = self_obj[tableName, "date"]
  priceXpath  = self_obj[tableName, "price"] 
  
  headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0'}
 
  try:
    page=requests.get(web, headers=headers)
  except:
    print "ERROR: Website not available: ", web 
    sys.exit(0)

  ## Check if the web data is sucessfully parsed
  if(page.status_code != requests.codes.ok):
    print "ERROR: Website Data was not available, The Website could be down or permissions might have been removed, Please check "
    print "Message: ", page.content  
    sys.exit(0)

  tree = html.fromstring(page.content)    
 

#  web = "/home/sudhiram/Desktop/gold.html"
#  with open(web, "r") as f:
#    page = f.read()
#  tree = html.fromstring(page)

#  error = filter(lambda x: re.search(r'Error', x, re.IGNORECASE), tree.xpath('//text()'))
#  if(error):
#    print "ERROR: Website is not available , Try again Later \n\t\t", web
#    print "\n\n ", error

  date  = tree.xpath(dateXpath)
  price = tree.xpath(priceXpath) 
  
  for i in range(len(date)):
    new_date = format_date(date[i])
    query = "INSERT INTO " + tableName + " VALUES (\"" + new_date + "\",\""+ price[i] + "\")"
    cur.execute(query)
    if(debug == 1):
      print "[DEBUG] ", tableName, ", ", new_date , ":", price[i] 
  
    
def parse_options():     
  global debug 
  
  try:
    opts, args = getopt.getopt(sys.argv[1:], "h", ["h","debug"])
  except getopt.GetoptError as err:
    print str(err)
    usage()
  
  for key, value in opts:
    if("--h" in key):
      usage()
    elif("--debug" in key):
      debug = 1
  
## Print Usage information to user and exit 
def usage(): 
    print "\nUsage: " , sys.argv[0] , "  "
    print "--------------------------------------------------------------"
    print "Absolutely NO Inputs !!"
    print ""
    print ""
    sys.exit(2)

if __name__ == "__main__":
    main()  
