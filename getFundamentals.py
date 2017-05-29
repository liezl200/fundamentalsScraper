#!/usr/bin/python
import os
import sys
import time
import tkMessageBox
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import glob

'''
GLOBAL CONSTANTS AND VARIABLES
'''
# where all the CSV files will go
STOCK_DIR = '/Users/liezl/Downloads'

# should be a file that has one stock symbol per line
STOCK_LIST_FILENAME = './stocklist.txt'

# should be a file that has one stock symbol per line
RETRY_LIST_FILENAME = './retryList.txt'

# file for the output csv
FIVE_YEAR_FUNDAMENTALS_FNAME = './five_year_fundamentals.csv'

# the names of the fundamentals we want to scrape
# we can calculate:
#   PE Ratio * Net Income = Market Cap
#   revenue/employee
#   net income / shares outstanding = annual earnings / share
# FUNDAMENTAL_CATEGORIES = ['revenue', 'employees', 'net income', 'shares outstanding', 'P%2FE ratio']
FUNDAMENTAL_CATEGORIES = ['P%2FE ratio']

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
# makes a new directory if it doesn't exist
def makeDir(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)

# read every line into a list of lines from fname, then return the list
def readListFromFile(fname):
  with open(fname) as f:
    lines = f.readlines()
    lineList = [x.strip() for x in lines]
    return lineList

# file should have username on first line then password on second line
def readUserInfoFromFile(fname):
  with open(fname) as f:
    lines = f.readlines()
    lineList = [x.strip() for x in lines]
    return lineList[0], lineList[1]

def signIntoWolfram(userInfoFilename):
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
  try:
    # have to click the Sign In button anytime we use driver.get() because Wolfram is bad at cookies
    signInBtn2 = driver.find_element_by_xpath('//*[@id="wa-user-menu"]/button[1]')
    signInBtn2.click()
  except:
    pass
  time.sleep(15) # wait 20 seconds for queried page to render
  driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
  footer = driver.find_element_by_xpath('//*[contains(@id, "HistoryQuarterly")]')
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
  time.sleep(15)

def downloadFundamentalCSVs(stockSymbols):
  for symbol in stockSymbols:
    for fundamental in FUNDAMENTAL_CATEGORIES:
      try:
        downloadOneFundamentalCSV(symbol, fundamental)
      except:
        print 'failed to download ', symbol, fundamental
    print 'finished downloading ' + symbol

def getCSVFilename(symbol, fundamental):
  fundamentalFileName = fundamental.replace('%2F', '_').replace(' ', '_').replace('.', '_')
  CSVfilenames = glob.glob(STOCK_DIR + '/*.csv')
  for filename in CSVfilenames:
    if fundamentalFileName.lower() in filename.lower() and symbol.lower() + '_' in filename.lower():
      return filename
  return None

def CSVExists(symbol, fundamental):
  return getCSVFilename(symbol, fundamental) != None

def retryDownloads(retrySymbols):
  successful = True
  for symbol in retrySymbols:
    for fundamental in FUNDAMENTAL_CATEGORIES:
      try:
        if not CSVExists(symbol, fundamental):
          downloadOneFundamentalCSV('NYSE:' + symbol, fundamental)
          print 'successful download retry of ', symbol, fundamental
      except:
        successful = False
        print 'failed to download ', symbol, fundamental
    print 'finished downloading ' + symbol
  # return successful

  # the rest of the code in this function only works if the STOCK_DIR is the same as the user's Downloads folder
  if not successful:
    return False
  # we have to double-check if we REALLY successfully downloaded everything, because Wolfram could have
  # errored out even if we successfully clicked all the buttons we needed to
  for symbol in retrySymbols:
    for fundamental in FUNDAMENTAL_CATEGORIES:
      if not CSVExists(symbol, fundamental):
        return False
  return True


signIntoWolfram('userinfo.txt')
stockSymbols = readListFromFile(STOCK_LIST_FILENAME)
# downloadFundamentalCSVs(stockSymbols) # if already downloaded, comment this out
retrySymbols = readListFromFile(STOCK_LIST_FILENAME)
while not retryDownloads(retrySymbols): # keep trying
  continue
