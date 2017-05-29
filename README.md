# fundamentalsScraper
Scrape stock fundamentals data from Wolfram Alpha Pro

## Prerequisites
1. Install Selenium for Python
2. Install Chrome Driver
- Download the latest chromedriver from https://sites.google.com/a/chromium.org/chromedriver/downloads
- Extract the chromedriver and then update the below path to point to the chromedriver executable
- Current version I'm using: https://chromedriver.storage.googleapis.com/2.29/chromedriver_mac64.zip

## Input / Output

1. Input: `stocklist.txt` is a list of symbols to scrape the data for. Format:

```
MMM
ABT
ABBV
ACN
ATVI
AYI
...
```

1. Output: `five_year_500.csv` a matrix of fundamentals

## How to run
`python getFundamentals.py`