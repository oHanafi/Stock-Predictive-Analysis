import urllib2 
import time
import datetime
import pyodbc
import json

from time import gmtime, strftime
stockToPull = ['AAPL', 'MSFT','GOOG', 'TSLA', 'AMD', 'INTC','NVDA', 'QCOM', 'NXPI', 'ASML', 'HPQ']

def fetchMarket(symbol):         
        cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=85.214.62.99;DATABASE=DatabaseSPA;UID=EXCEL;PWD=ibbeltje', timeout=3)
        cursor = cnxn.cursor()
       
        querryString = "SELECT stock_id FROM [Stock] WHERE Short = '" + symbol + "'"
        stockID = cursor.execute(querryString).fetchone()[0]    

        link = ("http://finance.google.com/finance/info?q=")
        url = link+"%s" % (symbol)
        u = urllib2.urlopen(url)
        content = u.read()
        data = json.loads(content[3:])
        info = data[0]
        t = str(info["lt"])    
        l = str(info["l"])    
        print t
        string = ("insert into [data](Stock_ID,Stock_Time,Closing) values("+str(stockID)+","+str(datetime.datetime.now().date())+","+str(l)+")")
        cursor.execute(string)


while True:
        for i in stockToPull:
            print (i)
            fetchMarket(i)
        time.sleep(60)
    
