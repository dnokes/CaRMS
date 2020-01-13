# -*- coding: utf-8 -*-
"""
Created on Thu Jan 09 10:29:35 2020

@author: Derek G Nokes
"""

import pandas
import requests
import datetime
from bs4 import BeautifulSoup
import xlrd
import dateutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


def downloadFile(url,outputDirectory,outputFileName):

    # start a session
    s = requests.session()

    # set the parameters
    parameters = {'siteEntryPassthrough': True}
 
    # try to extract the data
    try:
        # fetch the data
        r = s.get(url, params=parameters)                              
        # open the output file handle                                       
        outputFileHandle = open(outputDirectory+outputFileName,'wb')
        # write the holdings
        outputFileHandle.write(str(r.content))
        # close the file handle
        outputFileHandle.close()
                
    except Exception: 
        pass    
        
    return

# fetch data download links
def fetchDownloadLinks(baseUrl):
    # start a session
    s = requests.session()
    # set the parameters
    parameters = {'siteEntryPassthrough': True}
    # fetch the page
    response = s.get(baseUrl, params=parameters)    
    #  
    soup = BeautifulSoup(response.text,"lxml")
    # find all of the links
    links=soup.findAll("a")
    # iterate over all of the links
    
    downloadLinks=list()
    
    for link in links:
        # if the link contains 'ajax?fileType=csv&amp;fileName'
        if 'xls' in str(link):
            # extract the link
            downloadLink=link.attrs['href']
            # add to list
            downloadLinks.append(downloadLink)
        
    return downloadLinks

def fetchDataYears(baseUrl):
    
    driver = webdriver.Chrome()
    
    driver.get(baseUrl)
    
    time.sleep(5)
    
    pageSource=driver.page_source
    
    soup=BeautifulSoup(pageSource,'html.parser')
    
    years=soup.find(id='report-year-selector')
    
    yearsList=list()
    
    for year in years:
        try:
            yearsList.append(int(year.contents[0]))
        except:
            pass    
    
    driver.quit()
    
    return yearsList

def iterateOverYears():
    
    for year in yearsList:
        
    
    return

def fetchReports(driver,outputDirectory):
  
    pageSource=driver.page_source
    
    soup=BeautifulSoup(pageSource,'html.parser')
    
    # find all of the links
    links=soup.findAll("a")
    # iterate over all of the links

    downloadLinks=list()

    for link in links:
        # if the link contains 'ajax?fileType=csv&amp;fileName'
        if 'pdf' in str(link):
            # extract the link
            downloadLink=link.attrs['href']
            # add to list
            downloadLinks.append(downloadLink)   

    for downloadLink in downloadLinks:
        print(downloadLink)
        outputFileName=str(downloadLink.split('/')[-1])
        downloadFile(downloadLink,outputDirectory,outputFileName)
    
    return downloadLinks


# https://www.carms.ca/wp-content/uploads/2019/05/2019_r1_tbl1e.xlsx

# run these three in python console
baseUrl="https://www.carms.ca/data-reports/r1-data-reports/"
driver = webdriver.Chrome()
driver.get(baseUrl)

# select manually year in chrome window that pops up then run the function below for each selection

downloadLinks=fetchReports(driver,outputDirectory)

# close when finished
driver.quit()