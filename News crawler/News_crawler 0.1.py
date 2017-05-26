import requests
import json
import urllib
from bs4 import BeautifulSoup
from textblob import TextBlob
import feedparser
import pytest
import pyodbc
import sys
import re

# List with stocks. This has to be replaced with a database request for version 0.2.
stockToPull = 'AAPL', 'MSFT','GOOG', 'TSLA', 'AMD', 'INTC','NVDA', 'QCOM', 'NXPI', 'ASML', 'HPQ'
def connectDatabase():
        cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=ProjectSPA_2;UID=;PWD=')
        cursor = cnxn.cursor()
        querryString = "SELECT Short FROM Stock"
        cursor.execute(querryString)
        data = cursor.fetchall()
        cursor.close()
        return data

def addToNews(title, content, author, link, post_time):
        cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=ProjectSPA_2;UID=;PWD=')
        cursor = cnxn.cursor()
        cursor.execute("exec spAddNews '" + title + "', '" + content + "', '" + author + "', '" + link + "', '" + post_time + "'")
        cursor.commit()
        cursor.close()
        
def companyList():
        companies = []
        for stock in connectDatabase():
                stock = str(stock)[int(str(stock).find("'"))+1:]
                stock = stock[:int(str(stock).find("'"))]
                companies.append(stock)
        return companies        

def pullNews(stock):

    for stock in companyList():
            url = "http://www.marketwatch.com/investing/stock/" + stock + "/news"
            html = urllib.urlopen(url).read()
            soup = BeautifulSoup(html, "html.parser")
            
            listNews = soup.findAll('li', {"class" : "fnewsitem"})
            listWriters = soup.findAll('p', {"class" : "source"})
            
            listWriters = list(listWriters)
           

##            for writer in listWriters:
##                    writer = str(writer)[int(str(writer).find('-'))+2 :]
##                    writer = writer[:int(str(writer).find('<'))]             
##                    print(writer)

            PolaritySum = 0
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

##                    for author_tag in soup2.find_all('module-header'):
##                        Author = author_tag.text
##                        print author_tag.text    

                    listWriters = soup2.findAll('h3', {"class" : "module-header"})
                    Author = ""

                    for module in listWriters:
                            if str(module).count("href") == 0 and str(module).count("Bulletin") == 0 and str(module).count("References") == 0 and str(module).count("Popular") == 0 and str(module).count("Partner Center") == 0:
                                    Author = str(module)
                                    
                                    break
                            else:
                                    continue

                
                    
                    

                    
                    if Author:
                            Author = Author[int(Author.find('>'))+1:]
                            Author = Author[:int(Author.find('</b>'))]
                            Author = " ".join(Author.split())
                            Author = Author[:Author.index("<")]+ " " + Author[Author.index(">")+1:]
                            
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

                                
                    print Author            
                                
                
                    Content = ""
                    for paragraph_tag in soup2.find_all('p'):
                        #print paragraph_tag.text
                        Content = Content + paragraph_tag.text

                    Content = Content[int(Content.find('By')) + 2:]
                    Content = Content[:int(Content.find('Join the conversation'))]
                
                    Content = " ".join(Content.split())
                    #print(Content)
                    #addToNews(Title, Content, 'ja' ,'ja', '2014/12/20 10:12:30')
                    AnalyseThis = TextBlob(Content)
                    print ("Sentiment: " + str(AnalyseThis.sentiment.polarity))
                    PolaritySum = PolaritySum + AnalyseThis.sentiment.polarity

                    # The article has to be placed in the database for version 0.2.
                    print ("\n")
                    print ("=====================================================")
                    print ("\n")
    print PolaritySum/80
x = -10
while x < 0:
    for eachStock in companyList():
        pullNews(eachStock)
        

    print ("10 minute break \n")
    time.sleep(600)
    
