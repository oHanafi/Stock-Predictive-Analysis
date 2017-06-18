# -*- coding: cp1252 -*-
import requests
import json
import urllib
import urllib2 
from bs4 import BeautifulSoup
from textblob import TextBlob
import feedparser
import pytest
import pyodbc
import sys
import re
import datetime
from datetime import datetime
import pymssql
import time

# List with stocks. This has to be replaced with a database request for version 0.2.
stockToPull = 'AAPL', 'MSFT','GOOG', 'TSLA', 'AMD', 'INTC','NVDA', 'QCOM', 'NXPI', 'ASML', 'HPQ'
def getShort():
        cnxn = pymssql.connect( server='85.214.62.99', user='Excel', password='ibbeltje', database='ProjectSPA')
        cursor = cnxn.cursor()
        querryString = "SELECT Short FROM Stock"
        cursor.execute(querryString)
        data = cursor.fetchall()
        cursor.close()
        return data

def getStockID(short):
        cnxn = pymssql.connect( server='85.214.62.99', user='Excel', password='ibbeltje', database='ProjectSPA')
        cursor = cnxn.cursor()
        querryString = "SELECT Stock_ID FROM Stock where Short = '" + short + "'"
        cursor.execute(querryString)
        data = cursor.fetchone()
        for row in data:
                data = row
                break        
        cursor.close()
        return data

def addToNews(Stock, title, content, author, link, post_time, polarity, subjectivity):
        cnxn = pymssql.connect( server='85.214.62.99', user='Excel', password='ibbeltje', database='ProjectSPA')
        cursor = cnxn.cursor()
        print "hallo"
        string = ("inset into %d, %s, %s,%s,%s,%s,%s,%s,%s,%s)")
        cursor.execute(string,(str(Stock),str(title),str(content),str(author),str(link),str(post_time),str(polarity),str(subjectivity)))
        cnxn.commit()
        cursor.close()
        
def replace_index(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])

def companyList():
        companies = []
        for stock in getShort():
                stock = str(stock)[int(str(stock).find("'"))+1:]
                stock = stock[:int(str(stock).find("'"))]
                companies.append(stock)
        return companies        

def pullNews(stock):
        try:
        
                    for stock in companyList():
                            url = "http://www.marketwatch.com/investing/stock/" + stock + "/news"
                            html = urllib.urlopen(url).read()
                            soup = BeautifulSoup(html, "html.parser")
                            
                            listNews = soup.findAll('li', {"class" : "fnewsitem"})
                            listWriters = soup.findAll('p', {"class" : "source"})
                            
                            listWriters = list(listWriters)
                            StockID = getStockID(stock)
                            print type(StockID)
                            print str(StockID)
                            

                ##            for writer in listWriters:
                ##                    writer = str(writer)[int(str(writer).find('-'))+2 :]
                ##                    writer = writer[:int(str(writer).find('<'))]             
                ##                    print(writer)

                            PolaritySum = 0
                            #Er wordt voor elke link het artikel, titel, link, schrijver, post tijd en ophaaltijd opgehaald.
                            for links in listNews:
                                link = str(links)[int(str(links).find('/story')):]
                                link = link[:int(str(link).find('"'))]

                                # Database has to be checked if link is existing for version 0.2.
                                
                                if link: # Check if link is not empty
                

                                    link = "http://www.marketwatch.com" + link
                                    print(link)
                                    html = urllib.urlopen(link).read()
                                    Title = ""
                                    Author = ""
                                    soup2 = BeautifulSoup(html, "html.parser")
                                    for headline_tag in soup2.find_all('h1'):
                                        Title = headline_tag.text
                                        print headline_tag.text
                  

                                    listWriters = soup2.findAll('h3', {"class" : "module-header"})
                                    Author = ""

                                    for module in listWriters:
                                            if str(module).count("href") == 0 and str(module).count("countdown") == 0 and str(module).count("Bulletin") == 0 and str(module).count("References") == 0 and str(module).count("Popular") == 0 and str(module).count("Partner Center") == 0:
                                                    Author = str(module)
                                                    
                                                    break
                                            else:
                                                    continue
                                    if Author:
                                            Author = Author[int(Author.find('>'))+1:]
                                            Author = Author.replace('<b>', ' ')
                                            Author = Author.replace('</b>', '')
                                            Author = Author.replace('</h3>', '')
                                            print Author
                                            Author = re.sub(' +', ' ',Author)
                                            print Author
                                    else:
                                            Author = "Press release"
                                            
                                    if Author == "Press release":
                                        
                                        for par in soup2.find_all('p'):
                                                #print paragraph_tag.text
                                                if str(par).count("SOURCE") == 1:                                    
                                                        Author = str(par)[str(par).index("SOURCE")+7:]
                                                        Author = " ".join(Author.split())
                                                        Author = Author[:Author.index("<")]
                                                        break

                                    Content = ""
                                    for paragraph_tag in soup2.find_all('p'):
                                        #print paragraph_tag.text
                                        Content = Content + paragraph_tag.text
                                    #print Content
                                    Posting = ""
                                    Posting = soup2.findAll('p', {"id" : "published-timestamp"})
                                    print Posting
                                    pos = re.search("<span>", str(Posting))
                                    if pos.start():
                                            print pos.start()
                                    else:
                                            print "missing"
                                    Posting = str(Posting)[pos.start() + 6:]
                                    print Posting
                                    pos = re.search("</span>", str(Posting))
                                    Posting = str(Posting)[:pos.start()-3]
                                    print Posting
                                    

                                    Content = Content[int(Content.find('By')) + 2:]
                                    Content = Content[:int(Content.find('Join the conversation'))]
                                    #print "This is the time:  " + Posting
                                    
                                    
                                
                                    Content = " ".join(Content.split())
                                    #print Content
                                    #print(Content)
                                    AnalyseThis = TextBlob(Content)
                                    Title = Title.replace("'", "#sq#")
                                    Title = Title.replace('"', '#dq#')
                                    Content = Content.replace("'", "#sq#")
                                    Content = Content.replace('"', '#dq#')
                                    #Content = Content.replace('%', '#per#')
                                    #Content = Content.replace('©', '#cr#')
                                    Posting = Posting.replace("Published: ", "")
                                    Posting = Posting.replace(",", "")
                                    Posting = Posting.replace(".", "")
                                    Posting = Posting.replace(" am", "AM")
                                    Posting = Posting.replace(" pm", "PM")
                                    Posting = Posting.replace("Apr", "April")
                                    Posting = Posting.replace("Mar", "March")
                                    Posting = Posting.replace("Jan", "January")
                                    Posting = Posting.replace("Feb", "February")                
                                    
                                    Posting = Posting.replace("Aug", "August")
                                    Posting = Posting.replace("Sept", "September")
                                    Posting = Posting.replace("Oct", "October")
                                    Posting = Posting.replace("Nov", "November")
                                    Posting = Posting.replace("Dec", "December")
                                    print Posting
                                    #print "This is: " + Posting
                                    pos = re.search("\d", Posting)
                                    print Posting[pos.start()]
                                    print Posting[pos.start()-1]
                                    print Posting[pos.start()+1]
                                    if pos:
                                            if str(Posting)[pos.start() - 1] == " " and str(Posting)[pos.start() + 1] == " ": 
                                                    Posting = str(Posting)[:int(pos.start())] + Posting[pos.start()].zfill(2) + " " + Posting[int(pos.start()) + 2:]
                                    
                                    print  Posting

                                    pos = re.search(":", Posting) 
                                    print Posting
                                    if pos:
                                            if str(Posting)[pos.start() - 2] == " ":               
                                                    Posting = str(Posting)[:int(pos.start() - 1)] + str(Posting)[pos.start() - 1].zfill(2) + str(Posting)[int(pos.start()):]
                                    print Posting
                                    pos1 = re.search("a.m." or "p.m.", Posting)
                                    
                                    
                                    
                                    #print "This is the 2nd: " + Posting
                                    print ("Sentiment: " + str(AnalyseThis.sentiment.polarity))
                                    #PolaritySum = PolaritySum + AnalyseThis.sentiment.polarity
                                    Polarity = TextBlob(Content).sentiment.polarity
                                    Subjectivity = TextBlob(Content).sentiment.subjectivity
                                    print "Polarity: " + str(Polarity)
                                    print "Subjectivity: " + str(Subjectivity)
                                    


                                    print datetime.strptime(str(Posting), "%B %d %Y %I:%M%p")
                                    cnxn = pymssql.connect( server='85.214.62.99', user='Excel', password='ibbeltje', database='ProjectSPA')
                                    cursor = cnxn.cursor()
                                    print "hallo"
                                    string = ("insert into [NewsArticle](Stock_ID,Title,Content,Author,Link,Post_Time,Logg_Time,Polarity,Subjectivity) values(%d, %s, %s,%s,%s,%s,%s,%s,%s)")
                                    cursor.execute(string,(StockID, Title, Content, Author , link, Posting, datetime.now(), Polarity, Subjectivity))
                                    cnxn.commit()
                                    cursor.close()
                                    #addToNews(StockID, Title, Content, Author , link, Posting, Polarity, Subjectivity)
                                    
                                    # The article has to be placed in the database for version 0.2.
                                    print ("\n")
                                    print ("=====================================================")
                                    print ("\n")
                                    for eachStock in companyList():   
                                        fetchMarket(eachStock)

        except: 
                pass
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
                link = ("http://finance.google.com/finance/info?q=")
                url = link+"%s" % (symbol)
                u = urllib2.urlopen(url)
                content = u.read()
                data = json.loads(content[3:])
                info = data[0]
                t = str(info["lt"])    
                l = str(info["l"])    
                print symbol,t,l
                string = ("insert into [StockData](Stock_ID,Stock_Time,Closing) values(%d, %s, %s)")
                cursor.execute(string,(StockID,str(datetime.now()),str(l)))
                cnxn.commit()
                time.sleep(20)
        except: 
                pass

      
x = -10
while x < 0:
        
    for eachStock in companyList():
        pullNews(eachStock)

