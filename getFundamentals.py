#!/usr/bin/python
import os
import sys
import time
import tkMessageBox
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

'''
GLOBAL CONSTANTS AND VARIABLES
'''
# where all the CSV files will go
STOCK_DIR = './rawCSV/'

# should be a file that has one stock symbol per line
STOCK_LIST_FILENAME = './stocklist.txt'

# file for the output csv
FIVE_YEAR_FUNDAMENTALS_FNAME = './five_year_500.csv'

# the names of the fundamentals we want to scrape
FUNDAMENTAL_CATEGORIES = ['P%2FE']

# global stock symbol list that should be read in from ./stocklist.txt
stockSymbols = []

# global list of dates
dateLabels = []

# see README for chromedriver instructions
chromedriver = "/Users/liezl/Desktop/Code/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)


'''
FUNCTIONS
'''
# file should have username on first line then password on second line
def readUserInfoFromFile(fname):
  with open(fname) as f:
    lines = f.readlines()
    lineList = [x.strip() for x in lines]
    return lineList[0], lineList[1]

def signIn(userInfoFilename):
  # get user's login info
  username, password = readUserInfoFromFile(userInfoFilename)

  # input login info into the login form
  driver.get('https://account.wolfram.com/auth/sign-in')
  userField = driver.find_element_by_xpath('//*[@id="email"]/input')
  userField.send_keys(username)
  passwordField = driver.find_element_by_xpath('//*[@id="password"]/input')
  passwordField.send_keys(password)
  signInBtn = driver.find_element_by_xpath('//*[@id="sign-in-btn"]')
  signInBtn.click()

# usage: downloadOneFundamentalCSV('GOOG', 'P%2FE')
def downloadOneFundamentalCSV(symbol, fundamental):
  # get URL with corresponding symbol + desired fundamental query
  driver.get('https://www.wolframalpha.com/input/?i=' + symbol + '+' + fundamental)
  # have to click the Sign In button anytime we use driver.get() because Wolfram is bad at cookies
  signInBtn2 = driver.find_element_by_xpath('//*[@id="wa-user-menu"]/button[1]')
  signInBtn2.click()
  time.sleep(20) # wait 20 seconds for queried page to render
  driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
  footer = driver.find_element_by_xpath('//*[@id="HistoryQuarterly:PriceEarningsRatio:FinancialData"]/section/div[1]')
  hover = ActionChains(driver).move_to_element(footer)
  hover.perform()

  dldata = driver.find_elements_by_xpath('//*[contains(text(), "Data")]') # last element found in the list is the true Download Data button
  for dl in dldata:
    try:
      dl.click()
    except:
      pass
      # print 'failed clicking on element ', dl # uncomment for debugging only

  selectCSV = driver.find_element_by_xpath('//*[@id="exportpod-pricing"]/div[1]/select/option[4]')
  selectCSV.click()

  finalDownload = driver.find_element_by_xpath('//*[@id="signin-dl"]')
  finalDownload.click()


signIn('userinfo.txt')
downloadOneFundamentalCSV('GOOG', 'P%2FE')


