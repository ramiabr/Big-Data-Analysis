# Web Data Analysis 
The Goal of this project is to Extract Financial data (Gold and Silver Prices) from website (investing.com) and Build a MySQL database in local server, then code will perform various data analysis like compute Mean, Variance on the Dataset.   

## Architecture of Solution
This project contains two parts 

1.) Extract Data from Website (fetchHtml.py) 

2.) Perform Data Analysis on MySQL db (getCommodityPrice.py)
    
## fetchHtml.py     
- This program Extracts Gold and Silver Prices from investing.com website 
- As First Step the program builds MySQL database "goldSilverPrices" 
- MySQL database will have two tables gold and silver which will store 
  corresponding Price Data from website 
- The website will be parsed using Xpath module
- Parsed information is stored in database 

## getCommodityPrice.py
- This program will read My SQL Database for gold and silver tables
- Compute Mean (x1 + x2 + x3 +  ... + xn)/n 
- Variance (1/(n-1)) * ( (x1-M)^2 + (x2-M)^2 + ..... + (Xn-M)^2 )
- Print the output <Metal type> <Mean> <Variance>

## Scalability :
These two codes are built with high scalability as framework, for e.g. if we need the script to work on more types of data (e.g. Bronze, along with Gold + Silver) we need to make very few updates in the code to support that requirement. 

fetchHtml.py - Fill details for new element (e.g. Bronze), website to track, table id etc.
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
# Parse Website Gold website
parse_websites("gold")
```

getCommodityPrice.py
```
Does not need any modifications and Ready already  

```

## Built With 
- MySQLdb
- lxml
- requests
- Python 2.7

## Author
* **Ramkumar Subramanian** - *Initial work* - [rsubramanian@scu.edu]
