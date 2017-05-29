#!/usr/bin/python
import os
import sys
import time
import tkMessageBox
print sys.path
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

# CHROME DRIVER INSTRUCTIONS
# Download the latest chromedriver from https://sites.google.com/a/chromium.org/chromedriver/downloads
# Extract the chromedriver and then update the below path to point to the chromedriver executable
# Current version I'm using: https://chromedriver.storage.googleapis.com/2.29/chromedriver_mac64.zip
chromedriver = "/Users/liezl/Desktop/Code/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

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

signIn('userinfo.txt')

driver.get('https://www.wolframalpha.com/input/?i=GOOG+P%2FE')
# have to click the Sign In button anytime we use driver.get() because Wolfram is bad at cookies
signInBtn2 = driver.find_element_by_xpath('//*[@id="wa-user-menu"]/button[1]')
signInBtn2.click()
time.sleep(20) # wait for queried page to render
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