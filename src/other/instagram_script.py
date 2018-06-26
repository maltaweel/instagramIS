'''
Created on Dec 21, 2017

@author: TDBP1

Module to webscrape Instagram geotag photos for
caption, image link, and date information using Selenium.

Stores data in MongoDB.

'''

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from convert_datetime import ConvertDateTime
from emoji import UNICODE_EMOJI
from wheel.util import utf8
from run_mongo import mongo
from selenium.common.exceptions import NoSuchElementException

class InstaScraper:

    '''
    Initialization
    
    @param driverLocation: selenium driver location
    @param ls: Geotag URL code
    @param num: number of photos to be webscraped
    '''
    def __init__(self,driverLocation,ls,num):
        self.driverLocation=driverLocation
        self.list=ls
        self.num=num

    '''
    Method to run selenium webscraper and store data in MongodDB
    '''
        
    def runScraper(self):
        
        #connects to Chrome selenium driver
        browser=webdriver.Chrome()
        
        #base url to which self.list will be appended
        base_url=u'https://www.instagram.com/explore/locations/'
        
        #connect to MongoDB
#       m=mongo(self.list[0])
    
        #counter
        x=0

        for i in self.list:
        
            #append self.list to base_url
            query=unicode(i,"utf-8")
            url=base_url + query

            browser.get(url)
            time.sleep(1)
            
            #get the location information from the webpage.
            title=browser.find_element_by_tag_name('title').get_attribute('innerHTML')
            
            #print location to confirm correction location
            print('Location: '+title)
            
            #webdriver will be autoscrolling in html body
            body=browser.find_element_by_tag_name('body')
         
            
            for i in range(self.num):
                
                #autoscroll
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.2)                    
                
                #first 9 Instagrams on website are 'Top Posts'. 
                #Want to being scraping 'Most Recent' rather than 'Top Posts'
                if i<9:
                    continue
                
                #begin to scrape 'Most Recent' posts    
                else:
                    
                    #function to find correct Xpath
                    rem=(i-9)%3 +1
                    div= (i-9)//3 +1
                    
                    '''
                    Note: On Friday Jan 12, 2017
                    Instagram changed xpathDateTime from 
                    '/html/body/div[3]/div/div[2]/div/article/div[2]/div[2]/a/time'
                    to
                    '/html/body/div[4]/div/div[2]/div/article/div[2]/div[2]/a/time'
                    and changed xpathClose from
                    '/html/body/div[3]/div/button'
                    to
                    '/html/body/div[4]/div/button'
                    
                    If program is not working, or selenium gives 'TimeOutError,' it is likely
                    that Instagram changed some xpaths and the variables below need to be changed.
                    '''
                   
                    #xpath to individual post link
                    xpath3='//*[@id="react-root"]/section/main/article/div[2]/div[1]/div['+str(div)+']/div['+str(rem)+']/a'
                    
                    #xpath to post caption
                    xpath4='//*[@id="react-root"]/section/main/article/div[2]/div[1]/div['+str(div)+']/div['+str(rem)+']/a/div/div[1]/img'
                    
                    #xpathLoad='//*[@id="react-root"]/section/main/article/div[2]/a'
                    
                    #xpath to Date/Time information of post
                    xpathDateTime='/html/body/div[4]/div/div[2]/div/article/div[2]/div[2]/a/time'

                    #xpath to close button
                    xpathClose='/html/body/div[4]/div/button'

                    try:
                        #get caption
                        caption=browser.find_element_by_xpath(xpath4).get_attribute('alt')
                    
                    #if there are no more posts to scrape, stop scraping    
                    except NoSuchElementException:
                        browser.close()
                        break
                    
                    #get jpg link
                    link=browser.find_element_by_xpath(xpath4).get_attribute('src')
                    
                    #click on post link
                    openLink=browser.find_element_by_xpath(xpath3).click()
             
                    #wait until date/time information is visible
                    wait = WebDriverWait(browser, 10);
                    wait.until(EC.visibility_of_element_located((By.XPATH,xpathDateTime )));
                    
                    #get date/time information
                    dateTime=browser.find_element_by_xpath(xpathDateTime).get_attribute('datetime')
                    
                    #call on convert_datetimem module and getDate() method to convert
                    #the string into Date/Time format
                    convD=ConvertDateTime(dateTime).getDate()
                    
                    #click on the close button
                    closeLink= openLink=browser.find_element_by_xpath(xpathClose).click()
                    
                    #post to mongoDB using runinstamongo() method
                    m.runinstamongo(x+1, str(link), caption.encode('utf-8'), convD)
                    
                    #increase the counter
                    x=x+1
                                  
isC=InstaScraper()
isC.runScraper()

