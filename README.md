# Yellow Pages Scraper (YP-SCRAPER)

Yellowpages.com Web Scraper written in Python and LXML to extract business details available based on a particular category and location.
If you would like to know more about this scraper you can check it out at the blog post 'How to Scrape Business Details from Yellow Pages using Python and LXML' - https://www.scrapehero.com/how-to-scrape-business-details-from-yellowpages-com-using-python-and-lxml/

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Fields to Extract

This yellow pages scraper can extract the fields below:
'business_name', 'telephone', 'email', 'website', 'address', 'business_page'

### Prerequisites

For this web scraping tutorial using Python 3, we will need some packages for downloading and parsing the HTML.
Below are the package requirements:

- lxml
- requests
- unicodecsv
- urllib3

### Installation

PIP to install the following packages in Python (https://pip.pypa.io/en/stable/installing/)

Python Requests, to make requests and download the HTML content of the pages (http://docs.python-requests.org/en/master/user/install/)

Python LXML, for parsing the HTML Tree Structure using Xpaths (Learn how to install that here – http://lxml.de/installation.html)

## Running the scraper

We would execute the code with the script name followed by the positional arguments **keyword** and **place**. Here is an example
to find the business details for restaurants in Boston. MA.

```
python3 yp_scraper.py restaurants Boston,MA
```

## Thanks to

This repo is fork of https://github.com/scrapehero/yellowpages-scraper and all contribution goes to https://github.com/scrapehero

![Rocky road to yellow pages](https://media.giphy.com/media/g0snGpFL6mOBaD5PmO/giphy.gif)
