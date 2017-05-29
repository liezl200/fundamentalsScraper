# fundamentalsScraper
Scrape stock fundamentals data from Wolfram Alpha Pro

## Prerequisites
1. Install Selenium for Python
2. Install Chrome Driver
- Download the latest chromedriver from https://sites.google.com/a/chromium.org/chromedriver/downloads
- Extract the chromedriver and then update the below path to point to the chromedriver executable
- Current version I'm using: https://chromedriver.storage.googleapis.com/2.29/chromedriver_mac64.zip

## Input / Output of Main Functions

### `downloadFundamentalCSVs`
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

2. Output: Downloads the CSV files corresponding to the specified(stock, fundamental) combinations to the user's default Downloads folder.

### `retryDownloads`
1. Input: `retrylist.txt` is a list of stocks to download the fundamentals for (the function skips the download if the file already exists). `rawCSV` is a folder containing the successfully scraped raw CSVs from Wolfram

2. Output:` Downloads the missing CSV files corresponding to the specified(stock, fundamental) combinations to the user's default Downloads folder. Returns true if we successfully downloaded all the CSVs, false if not.

### `formatCSVs`
1. Input: `fundamentals`, a subset of the FUNDAMENTAL_CATEGORIES (default is the full list). `rawCSV` is a folder containing the raw CSVs from Wolfram.

2. Output:` `five_year_fundamentals.csv` a matrix of fundamentals. Any stocks missing one or more fundamentals will be ommitted from the matrix.

## How to run
`python getFundamentals.py`

## Workflow guidelines
1. `downloadFundamentalCSVs(stockSymbols)`
2. Copy all raw CSVs from your downloads folder into your repository folder.
3. Repeat `retryDownloads(stockSymbols)` until it returns True.
4. `formatCSVs(fundamentals)` -- note that any stocks with missing fundamentals will be ommitted.

Final Output: `five_year_fundamentals.csv`