import urllib2 
import time
import datetime

stockToPull = 'AAPL', 'MSFT','GOOG', 'TSLA'

tests = 
def pullData(stock):
    try:
        print 'Current pulling', stock
        print str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M-%S'))
        urlToVisit = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range=1d/csv'
        saveFileLine = stock+'.csv'
        try:
            readExistingData = open(saveFileLine,'r').read()
            splitExisting = readExistingData.split('\n')
            mostRecentLine = splitExisting[-2]
            lastUnix = mostRecentLine.split(',')[0] 
        except Exception,e:
            print "File did not exist yet",e
            lastUnix = 0
        saveFile = open(saveFileLine,'a')
        sourceCode = urllib2.urlopen(urlToVisit).read()
        splitSource = sourceCode.split('\n')

        for eachLine in splitSource:
            splitLine = eachLine.split(',')
            if len(splitLine) == 6:
                if 'values' not in eachLine:
                    if int(splitLine[0]) > int(lastUnix):
                        lineToWrite = eachLine+'\n'
                        saveFile.write(lineToWrite)
        saveFile.close()        
        print 'Pulled',stock
        print 'Sleeping'
        print str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M-%S'))
        time.sleep(5)
    except Exception,e:
        print 'main loop', str(e)

        test

for eachStock in stockToPull:
    pullData(eachStock)
    