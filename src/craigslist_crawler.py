'''

craigslist_crawler.py
by Ryan Delgado
'''

# standard Python libraries for manipulating strings dates
import os
import re
import json
import time
from datetime import datetime
import logging

# lxml/xpath for parsing the web pages
from lxml import html

# Selenium for clicking buttons & pagination
from selenium import webdriver

# Set up the logger
logger = logging.getLogger(__name__)

# Constants
SCRAPE_DATE = datetime.now()
DATA_DIR = os.path.join(os.getcwd(), 'data', SCRAPE_DATE.strftime('%Y%m%d'))
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
FILENAME_TEMPLATE = 'craigslist_newyork_{uniqueid}_{scrape_date}.json'

# Set up ChromeDriver
logger.info('Setting up ChromeDriver')
chromedriver = "./ChromeDriver/chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)


def scrape_page(listing_url):
    logger.info('Crawling {}'.format(listing_url))
    elementFound = True
    """try:
        # Click the reply button
        reply_button = driver.find_element_by_xpath('//button[@class="reply_button js-only"]')
        reply_button.click()
        elementFound = True
    except:
        print("couldn't find element")
        print(driver.page_source)
        raise ValueError("Something wen't wrong, look at the blob")
    """    

    if elementFound:
        # Extract the page source
        driver.get(listing_url)
        time.sleep(2)
        page = driver.page_source
    
        # Store the scraped page and metadata in a dictionary
        scrape_dict = {
            'scrape_date': SCRAPE_DATE.strftime('%Y-%m-%d')
            ,'body': page
            ,'url': driver.current_url
        }
    
        # Parse out the unique ID in the url to use in the filename
        unique_id = re.search('\/(\d+)\.html$', driver.current_url).group(1)
    
        # Save the file down
        filename = FILENAME_TEMPLATE.format(uniqueid=unique_id, scrape_date=SCRAPE_DATE.strftime('%Y%m%d'))
        filepath = os.path.join(DATA_DIR, filename)
        logger.info('Saving to {}'.format(filepath))
        with open(filepath, 'w') as f:
            json.dump(scrape_dict, f)
    
def crawl_page_listings():

    logger.info('Crawling the apartment links on {}'.format(driver.current_url))

    # Parse out the links to all of the apartment listings on the page
    page = driver.page_source
    tree = html.fromstring(page)
    listing_urls = tree.xpath('//a[@class="result-title hdrlnk"]/@href')

    # Crawl each listing url
    for listing_url in listing_urls:
        print(listing_url)
        scrape_page(listing_url)


def main():

    # Visit the start page
    START_URL = 'https://newyork.craigslist.org/d/rooms-shares/search/roo'
    driver.get(START_URL)

    # Paginate through the listing pages, crawling & scraping each listing link
    on_last_page = False
    while not on_last_page:
        # Record the current listing page so we can revisit it when we're finished crawling all of the listings.
        current_listing_page = driver.current_url

        # Crawl & scrape all of the apartment listings on this page
        crawl_page_listings()

        # Come back to the current listing page after the scrape is finished
        driver.get(current_listing_page)
        time.sleep(2)  # wait for the page to load

        # Click the 'Next' link
        logger.info('Visiting the next page.')
        driver.find_element_by_xpath('//a[@class="button next"]').click()
        time.sleep(2)

        # Check if we're on the last page
        on_last_page = ('no results' in driver.page_source)
        if on_last_page:
            logger.info('Crawler finished!')


if __name__ == '__main__':
    main()