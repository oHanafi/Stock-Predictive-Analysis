import urllib2 
import time
import datetime
import pymssql  
import json

from time import gmtime, strftime
stockToPull = ['AAPL', 'MSFT','GOOG', 'TSLA', 'AMD', 'INTC','NVDA', 'QCOM', 'NXPI', 'ASML', 'HPQ']

def fetchMarket(symbol):
        try:

                cnxn = pymssql.connect( server='85.214.62.99', user='Excel', password='ibbeltje', database='ProjectSPA')
                cursor = cnxn.cursor()
               
                querryString = "SELECT stock_id FROM [Stock] WHERE Short = '" + symbol + "'"
                stockID = cursor.execute(querryString)
                row = cursor.fetchone()
                while row:
                    StockID = (row[0])
                    row = cursor.fetchone()

                print StockID
                link = ("http://finance.google.com/finance/info?q=")
                url = link+"%s" % (symbol)
                u = urllib2.urlopen(url)
                content = u.read()
                data = json.loads(content[3:])
                info = data[0]
                t = str(info["lt"])    
                l = str(info["l"])
                print t,l

                string = ("insert into [StockData](Stock_ID,Stock_Time,Closing) values(%d, %s, %s)")
                cursor.execute(string,(StockID,str(datetime.datetime.now()),str(l)))
                cnxn.commit()
        except: 
                pass

      


while True:
        for i in stockToPull:
            print (i)
            fetchMarket(i)
        time.sleep(60)
    
