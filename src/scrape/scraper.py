'''
Created on Jun 25, 2018

@author: mark
'''
import time
from bs4 import BeautifulSoup
import requests
import json
from random import choice
from urllib2 import urlopen

from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

account='instagram'


def login(driver):
    username = "markaltaweel"   # Your username
    password = "prath4a5"   # Your password

    # Load page
    driver.get("https://www.instagram.com/accounts/login/")

    # Login
    driver.find_element_by_xpath("//div/input[@name='username']").send_keys(username)
    driver.find_element_by_xpath("//div/input[@name='password']").send_keys(password)
    driver.find_element_by_xpath("//span/button").click()

    # Wait for the login page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "See All")))

def scrape_page(tag):

    mainLink='https://www.instagram.com/explore/tags/'+tag+"/"
    page=driver.get(mainLink)
    
    json_data=extract_json_data(mainLink)
    entry=json_data['entry_data']
    for i in entry:
        q=entry[i]
        for n in range(0,len(q)):
            lst=q[n]
            for ff in lst:
                nt=lst[ff]
                hTag=nt['hashtag']['edge_hashtag_to_media']['edges']
                
                for ttt in range(0,len(hTag)):
                    node=hTag[ttt]
                    nd=node['node']['edge_media_to_caption']['edges']
                
                    for iii in range(0,len(nd)):
                            prts=nd[iii]
                            text=prts['node']['text']
                            print(text)
              

def extract_json_data(html):
        soup = BeautifulSoup(urlopen(html), 'html.parser')
        body = soup.find('body')
        script_tag = body.find('script')
        raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
        return json.loads(raw_string)
    
def scrape_followers(driver, account):
    # Load account page
    driver.get("https://www.instagram.com/{0}/".format(account))

    # Click the 'Follower(s)' link
    driver.find_element_by_partial_link_text("follower").click()

    # Wait for the followers modal to load
    xpath = "//div[@style='position: relative; z-index: 1;']/div/div[2]/div/div[1]"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    
    SCROLL_PAUSE = 0.5  # Pause to allow loading of content
    driver.execute_script("followersbox = document.getElementsByClassName('_gs38e')[0];")
    last_height = driver.execute_script("return followersbox.scrollHeight;")

    # We need to scroll the followers modal to ensure that all followers are loaded
    while True:
        driver.execute_script("followersbox.scrollTo(0, followersbox.scrollHeight);")

        # Wait for page to load
        time.sleep(SCROLL_PAUSE)

        # Calculate new scrollHeight and compare with the previous
        new_height = driver.execute_script("return followersbox.scrollHeight;")
        if new_height == last_height:
            break
        last_height = new_height

    # Finally, scrape the followers
    xpath = "/html/body/div[4]/div/div/div[2]/div/div[2]/ul/li"
    followers_elems = driver.find_elements_by_xpath(xpath)

    followers_temp = [e.text for e in followers_elems]  # List of followers (username, full name, follow text)
    followers = []  # List of followers (usernames only)

    # Go through each entry in the list, append the username to the followers list
    for i in followers_temp:
        username, sep, name = i.partition('\n')
        followers.append(username)

    print("______________________________________")
    print("FOLLOWERS")

    return followers

def scrape_following(driver, account):
    # Load account page
    driver.get("https://www.instagram.com/{0}/".format(account))

    # Click the 'Following' link
    driver.find_element_by_partial_link_text("following").click()

    # Wait for the following modal to load
    xpath = "/html/body/div[4]/div/div/div[2]/div/div[2]"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath)))

    SCROLL_PAUSE = 0.5  # Pause to allow loading of content
    driver.execute_script("followingbox = document.getElementsByClassName('_gs38e')[0];")
    last_height = driver.execute_script("return followingbox.scrollHeight;")

    # We need to scroll the following modal to ensure that all following are loaded
    while True:
        driver.execute_script("followingbox.scrollTo(0, followingbox.scrollHeight);")

        # Wait for page to load
        time.sleep(SCROLL_PAUSE)

        # Calculate new scrollHeight and compare with the previous
        new_height = driver.execute_script("return followingbox.scrollHeight;")
        if new_height == last_height:
            break
        last_height = new_height

    # Finally, scrape the following
    xpath = "/html/body/div[4]/div/div/div[2]/div/div[2]/ul/li"
    following_elems = driver.find_elements_by_xpath(xpath)

    following_temp = [e.text for e in following_elems]  # List of following (username, full name, follow text)
    following = []  # List of following (usernames only)

    # Go through each entry in the list, append the username to the following list
    for i in following_temp:
        username, sep, name = i.partition('\n')
        following.append(username)

    print("\n______________________________________")
    print("FOLLOWING")
    return following


if __name__ == "__main__":
    
    driver = wd.Chrome()
    try:
        login(driver)
        #followers = scrape_followers(driver, account)
        #print(followers)
        #following = scrape_following(driver, account)
        #print(following)
        scrape_page('ironage')
    finally:
        driver.quit()