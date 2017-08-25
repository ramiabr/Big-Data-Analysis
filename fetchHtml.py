#!/usr/bin/python
import sys, getopt
import os
import re

try:
  import MySQLdb
except:
  print "ERROR: \"MySQLdb\" module is not installed, please install and try again"
  sys.exit(0)

# Exception Handling for LXML module
try:
  from lxml import html
  import lxml.html as LH
except:
  print "ERROR: \"lxml\" package is not installed, Please install and try again (For Python 3: sudo apt-get install python3-lxml) \n "
  sys.exit(0)

 
try:
  import requests
except:
  print "ERROR: \"requests\" package is not installed, Please install and try again (pip install requests) \n "
  sys.exit(0)
  

## Global Variables
global debug 
global gold_address   
global silver_address 

# Global Var initialization
debug = 0
gold_address = "https://www.investing.com/commodities/gold-historical-data"
silver_address = "https://www.investing.com/commodities/silver-historical-data"


## Initializating Database
global db
global cur


def openDB():
  global db
  global cur
  
  db = MySQLdb.connect(host="localhost",  # your host 
     user="root",	   # username
     passwd="scu@123",     # password
     db="goldSilverPrices")   # name of the database
 
  # Create a Cursor object to execute queries.
  cur = db.cursor()

def deleteDataDB():
  global db
  global cur

  openDB()

  ## Wipe table clean
  
  #query = "TRUNCATE TABLE gold"
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

  db.commit()  
  closeDB()

def closeDB():
  global db
  global cur

  db.commit()
  db.close()


def main():  
  parse_options()
  deleteDataDB()
  db = parse_websites(gold_address, "gold_data.txt", "gold")
   
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

def parse_websites(web, db, tableName):  
#  try:
#    page=requests.get(web)
#  except:
#    print "ERROR: Website not available: ", web , 
#
#  tree = html.fromstring(page.content)
    

  web = "/home/sudhiram/Desktop/gold.html"
  with open(web, "r") as f:
    page = f.read()
  tree = html.fromstring(page)

  openDB()

  error = filter(lambda x: re.search(r'Error 403 You are banned', x), tree.xpath('//text()'))
  if(error):
    print "ERROR: You are banned from this site, Try again Later \n\t\t", web,

  date  = tree.xpath('//div[@id="results_box"]/table[@id="curr_table"]/tbody/tr/td[1]/text()')
  price = tree.xpath('//div[@id="results_box"]/table[@id="curr_table"]/tbody/tr/td[2]/text()') 
  
  for i in range(len(date)):
    new_date = format_date(date[i])
    query = "INSERT INTO " + tableName + " VALUES (\"" + new_date + "\",\""+ price[i] + "\")"
    cur.execute(query)
  
  closeDB()
  return db

    
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
  
  print "INFO: Parsing HTML Files"



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
