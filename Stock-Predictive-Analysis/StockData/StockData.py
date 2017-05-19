import urllib2 
import time
import datetime
import pyodbc


stockToPull = 'AAPL', 'MSFT','GOOG', 'TSLA', 'AMD', 'INTC','NVDA', 'QCOM', 'NXPI', 'ASML', 'HPQ'

def pullData(stock):
    try:
        print stock
        cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=H2675330\SQLEXPRESS;DATABASE=DatabaseSPA;UID=;PWD=')
        cursor = cnxn.cursor()
        querryString = "SELECT stock_id FROM [Stock] WHERE Short = '" + stock + "'"
        cursor.execute(querryString)
        rows = cursor.rowcount


        if rows <= 0:
            querryString = "insert into [Stock] values('" + stock + "','NULL')"
            cursor.execute(querryString)
            cursor.commit()
        querryString = "SELECT stock_id FROM [Stock] WHERE Short = '" + stock + "'"
        stockID = cursor.execute(querryString).fetchone()[0]    


        querryString = "SELECT Stock_Time FROM [Data] WHERE Stock_id = "+ str(stockID)
      
        rows = len(cursor.execute(querryString).fetchall())
        
        if rows <= 0:
            lastUnix = 0
            
        else:
            querryString = "SELECT max(Stock_Time) FROM [Data] WHERE Stock_id = "+ str(stockID)
            lastUnix = cursor.execute(querryString).fetchone()[0]
            


        print 'Current pulling', stock
        print str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M-%S'))
        urlToVisit = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range=1d/csv'
        sourceCode = urllib2.urlopen(urlToVisit).read()
        splitSource = sourceCode.split('\n')

        for eachLine in splitSource:
            splitLine = eachLine.split(',')
            if len(splitLine) == 6:
                if 'values' not in eachLine:
                    
                    if int(splitLine[0]) > int(lastUnix):
                        lineToWrite = eachLine+'\n'
                        stockTimeStamp = lineToWrite.split(',')[0]
                        stockClose = lineToWrite.split(',')[1]
                        stockHigh = lineToWrite.split(',')[2]
                        stockLow = lineToWrite.split(',')[3]
                        stockOpen = lineToWrite.split(',')[4]
                        stockVolume = lineToWrite.split(',')[5]
                        querryString = "insert into [Data] values(" + str(stockID) + "," + str(stockTimeStamp) + ",'" + str(stockClose) + "','" + str(stockHigh) + "','" + str(stockLow) + "','" + str(stockOpen) + "','" + str(stockVolume) + "',getdate())"

                        
                        cursor.execute(querryString)
                        cursor.commit()      
        print 'Pulled',stock
        print 'Sleeping'
        print str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M-%S'))
        print '\n'
        time.sleep(5)
    except Exception,e:
        print 'main loop', str(e)

x = -10
while x < 0:
    for eachStock in stockToPull:
        pullData(eachStock)

    print ("10 minute break \n")
    time.sleep(600)
    
