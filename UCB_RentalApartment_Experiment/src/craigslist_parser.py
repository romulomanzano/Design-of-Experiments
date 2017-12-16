
'''
craigslist_parser.py
by Ryan Delgado

'''

import os
import re
import json
from glob import glob
from datetime import datetime
import logging
from lxml import html
import pandas as pd

# Set up the logger
logger = logging.getLogger(__name__)

# Constants
SCRAPE_DATE = datetime.now()  # This assumes that the parser is run on the same day as the crawler.
DATA_DIR = os.path.join(os.getcwd(), 'data', SCRAPE_DATE.strftime('%Y%m%d'))

# Utility functions for cleaning up fields
def clean_neighborhood(neighborhood_text): return re.sub(r'[\(\)\s]', '', neighborhood_text)

def parse_posting_date(posting_datetime):
    posting_date = re.search(r'^(\d{4}\-\d{2}\-\d{2}).*', posting_datetime).group(1)
    return datetime.strptime(posting_date,'%Y-%m-%d')


def main():
    json_files = glob(DATA_DIR)

    scrape_data = []
    for jf in json_files:
        logger.info('Processing {}'.format(jf))

        # Read the .json file into a dictionary
        with open(jf, 'r') as f:
            scrape_dict = json.load(f)

        # Read the page source into an lxml etree
        tree = html.fromstring(scrape_dict['body'])

        # Parse out the contact email, title text, neighborhood, and posting date. Also include the url and date scraped.
        # Append to the scrape_data list.
        listing_dict = {
             # 'Contact Email': tree.xpath('//a[contains(@href,"mailto")]/text()')[0]
            'Title': tree.xpath('//span[@id="titletextonly"]/text()')[0]
            ,'Neighborhood': clean_neighborhood(tree.xpath('//span[@class="postingtitletext"]/small/text()')[0])
            ,'Posting Date': parse_posting_date(tree.xpath('//p[@id="display-date"]/time/@datetime')[0])
            ,'Scrape Date': scrape_dict['scrape_date']
            ,'url': scrape_dict['url']
            ,'Source File Name': jf
        }
        scrape_data.append(listing_dict)

    # Read the scrape results into a DataFrame. Write to a csv
    craigslist_df = pd.DataFrame(scrape_data)
    craigslist_df.to_csv('craigslist_nyapt_scrape_{}.csv'.format(SCRAPE_DATE.strftime('%Y%m%d')), encoding='utf-8')


if __name__ == '__main__':
    main()