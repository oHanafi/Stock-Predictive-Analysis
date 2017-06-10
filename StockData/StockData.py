import urllib2 
import time
import datetime
import pyodbc
import json


stockToPull = ['AAPL', 'MSFT','GOOG', 'TSLA', 'AMD', 'INTC','NVDA', 'QCOM', 'NXPI', 'ASML', 'HPQ']

def fetchMarket(symbol):         
        cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=85.214.62.99;DATABASE=DatabaseSPA;UID=EXCEL;PWD=ibbeltje', timeout=3)
        cursor = cnxn.cursor()
       
        querryString = "SELECT stock_id FROM [Stock] WHERE Short = '" + symbol + "'"
        stockID = cursor.execute(querryString).fetchone()[0]    

        print (stockID)
        link = ("http://finance.google.com/finance/info?q=")
        url = link+"%s" % (symbol)
        u = urllib2.urlopen(url)
        content = u.read()
        data = json.loads(content[3:])
        info = data[0]
        t = str(info["lt"])    
        l = str(info["l"])    
       
        cursor.execute("insert into [Data] values(" + str(stockID) + "," + str(t) + ",'" + str(l) + "','" + str(0) + "','" + str(0) + "','" + str(0) + "','" + str(0) + "'," +str(0)+")")
        cnxn.commit()
                

for i in stockToPull:
    print (i)
    fetchMarket(i)
time.sleep(60)
    
