# Web Data Analysis 
The Goal of this project is to Extract Financial data (Gold and Silver Prices) from website (investing.com) and Build a MySQL database in local server, then code will perform various data analysis like compute Mean, Variance on the Dataset.   

## Architecture
There are two parts 

1.) Extract Data from Website (fetchHtml.py) 

2.) Perform Data Analysis on MySQL db (getCommodityPrice.py)
    
## fetchHtml.py     
- This program Extracts Gold and Silver Prices from investing.com website 
- It also builds MySQL database "goldSilverPrices" in local server 
- MySQL database will have two tables gold and silver which will store 
  corresponding Price Data from website 
- Website will be parsed using Xpath module
- Parsed information is stored in MySQL database 

## getCommodityPrice.py
- This program will read My SQL Database for gold and silver tables
- Compute Mean (x1 + x2 + x3 +  ... + xn)/n 
- Variance (1/(n-1)) * ( (x1-M)^2 + (x2-M)^2 + ..... + (Xn-M)^2 )
- Print the output <Metal type> <Mean> <Variance>

## Scalability :
These two codes are built with high scalability, for e.g. if we need script to process more types of data (e.g. Bronze, along with Gold + Silver) we need to make very few updates in the code to support that requirement. 

fetchHtml.py - Paper Work !!
```
self_obj["silver", "web"]   = "https://www.investing.com/commodities/silver-historical-data"
self_obj["silver", "date"]  = "//div[@id=\"results_box\"]/table[@id=\"curr_table\"]/tbody/tr/td[1]/text()"
self_obj["silver", "price"] = "//div[@id=\"results_box\"]/table[@id=\"curr_table\"]/tbody/tr/td[2]/text()"
```

fetchHtml.py - Create new DB Table 
```
query = "drop table if exists silver"
cur.execute(query)
...
...
query = "CREATE TABLE silver(date DATE, price VARCHAR(20))"
cur.execute(query)
```

fetchHtml.py  - Enable parse website analyze new web data
```
parse_websites("gold")
```

getCommodityPrice.py
```
Ready !!
```

## Prerequisites 
- MySQLdb
- lxml
- requests
- Python 2.7
- MySQLdb "goldSilverPrices" db setup

## Author
* **Ramkumar Subramanian** - *Initial work* - [rsubramanian@scu.edu]

## Acknowledgments
I would like to Thank **Mr. Peter Walther** (VP, Big Data Federation, Inc) for being inspiration behind this project.
