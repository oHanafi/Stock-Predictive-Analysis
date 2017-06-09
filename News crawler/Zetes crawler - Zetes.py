
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
import csv
import goslate 
                

def pullNews():

   
        url = "https://www.tweakers.net/zoeken/?keyword=zetes"
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html, "html.parser")
            
        listNews = soup.findAll('p', {"class" : "title ellipsis"})
            
        Writer = "Tweakers"

        PolaritySum = 0

        for link in listNews:
                link = str(link)[int(str(link).find('href'))+6:]
                link = str(link)[:int(str(link).find('">'))]
                
                
        
                if link: # Check if link is not empty
                        
                        html = urllib.urlopen(link).read()
                        Title = ""
                        Author = ""
                        soup2 = BeautifulSoup(html, "html.parser")
                        news = []
  

                        news = soup2.findAll('p', {"class" : "lead"}) + soup2.findAll('img', {"class" : "alignRight"})
                        
                        # The article has to be placed in the database for version 0.2.
                        print ("\n")
                        print ("=====================================================")
                        print ("\n")
                        #print PolaritySum/80
                        lijstje = []

                        news = list(soup2.findAll('div', {"class" : "reactieContent"}))
                        for com in news:
                                com = str(com)[int(str(com).find('\n\t\t\t\t\t')):]
                                #com = com[:int(str(link).find('\n\t\t\t\t\t\n\t\t\t\t'))]
                                com = com.replace("\n\t\t\t\t\t\n\t\t\t\t</div>", " ")
                                com = " ".join(com.split())
                                #print com
                                print ("\n")
                                print ("=====================================================")
                                print ("\n")
                                print com
                        

                            
                            

                        
                        
                        

x = 0
while x < 1:
    pullNews()
    x = x+1
        

    
    
