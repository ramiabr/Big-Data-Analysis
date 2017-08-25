# Web Data Analysis 
The Goal of this project is to Extract Financial data (Gold and Silver Prices) from website (investing.com) and Build a MySQL database in local server, then code will perform various data analysis like compute Mean, Variance on the Dataset.   

## Running Steps
### Program 1:
#### Tables in MySQLdb are first empty    
The script expects to have a Database with the Tables. Attaching the goldSilverPrices.sql file for reference.  

```
mysql> SELECT * from gold;
Empty set (0.00 sec)

mysql> SELECT * from silver;
Empty set (0.00 sec)
```

#### Running fetchHtml.py script : Populating the DB  
```
ram@ubuntu:~/BigData$ ./fetchHtml.py
INFO: Parsing HTML :  https://www.investing.com/commodities/gold-historical-data
INFO: Parsing HTML :  https://www.investing.com/commodities/silver-historical-data

INFO: Flow completed successfully !!
```

#### Now checking the populated MySQLdb 
```
mysql> SELECT * from gold;
+------------+----------+
| date       | price    |
+------------+----------+
| 2017-08-25 | 1,292.14 |
| 2017-08-24 | 1,291.93 |
  ..........   ........
  ..........   ........
| 2017-07-26 | 1,255.60 |
| 2017-07-25 | 1,258.50 |
+------------+----------+

mysql> SELECT * from silver;
+------------+--------+
| date       | price  |
+------------+--------+
| 2017-08-25 | 16.965 |
| 2017-08-24 | 16.940 |
  ..........   ........
  ..........   ........
| 2017-07-26 | 16.459 |
| 2017-07-25 | 16.542 |
+------------+--------+
```

### Program 2:
#### Mean and variance of the commodity’s price over the specified date range
```
ram@ubuntu:~/BigData$ ./getCommodityPrice.py  2017-07-25 2017-08-25 gold
gold 1280.01 161.87 

ram@ubuntu:~/BigData$ ./getCommodityPrice.py  2017-07-25 2017-08-25 silver
silver 16.78 0.07 
```

## Prerequisites 
- MySQLdb
- lxml
- requests
- Python 2.7
- MySQLdb "goldSilverPrices" db setup
