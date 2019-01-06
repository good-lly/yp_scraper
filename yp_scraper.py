#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import html
import urllib3
import unicodecsv as csv
import argparse

urllib3.disable_warnings()
print(
        '''
        ==============================================
        |                                            |
        |                                            |
        |    🍌 WELCOME TO YELLOWPAGES SCRAPER!      |
        |                                            |
        |                                            |
        ==============================================
        '''
    )
def parse_listing(keyword, place):
    global page
    page = 1
    global scraped_results
    scraped_results = []
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Host': 'www.yellowpages.com',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
               }
    while page != 0:
        url = "https://www.yellowpages.com/search?search_terms={0}&geo_location_terms={1}&page={2}".format(keyword, place, page)
        # Adding retries
        print('')
        print('Fetching url: ', url)
        print('====================================')
        print('page: ', page)
        print('')
        try:
            response = requests.get(url, verify=False, headers=headers)
            if response.status_code == 200:
                parser = html.fromstring(response.text)
                # making links absolute
                base_url = "https://www.yellowpages.com"
                parser.make_links_absolute(base_url)

                XPATH_LISTINGS = "//div[@class='search-results organic']//div[@class='v-card']"
                listings = parser.xpath(XPATH_LISTINGS)
                if not listings:
                    page = 0
                    break
                else:
                    for results in listings:
                        XPATH_BUSINESS_NAME = ".//a[@class='business-name']//text()"
                        XPATH_BUSSINESS_PAGE = ".//a[@class='business-name']//@href"
                        XPATH_TELEPHONE = "//*[@id='main-header']//article//section[2]//div[1]//p[@class='phone']//text()"
                        XPATH_EMAIL = "//*[@id='main-header']/div/a[2]//@href"
                        XPATH_ADDRESS = "//*[@id='main-header']//article//section[2]//div[1]//p[@class='address']//text()"
                        XPATH_WEBSITE = ".//div[@class='info']//div[contains(@class,'info-section')]//div[@class='links']//a[contains(@class,'website')]/@href"

                        raw_business_name = results.xpath(XPATH_BUSINESS_NAME)
                        raw_business_page = results.xpath(XPATH_BUSSINESS_PAGE)
                        raw_website = results.xpath(XPATH_WEBSITE)
                        raw_email = ''
                        raw_business_telephone = ''
                        raw_address = ''

                        business_name = ''.join(raw_business_name).strip() if raw_business_name else None
                        business_page = ''.join(raw_business_page).strip() if raw_business_page else None

                        if business_page:
                            print("✅ " + business_name)
                            page_response = requests.get(business_page, verify=False, headers=headers)
                            if page_response.status_code == 200:
                                parsed_page = html.fromstring(page_response.text)
                                raw_email = parsed_page.xpath(XPATH_EMAIL)
                                raw_business_telephone = parsed_page.xpath(XPATH_TELEPHONE)
                                raw_address = parsed_page.xpath(XPATH_ADDRESS)
                        else:
                            print("❌ No business page for " + business_name)

                        email = ''.join(raw_email).strip() if raw_email else None
                        if email:
                            email = email[7:]

                        telephone = ''.join(raw_business_telephone).strip() if raw_business_telephone else None
                        website = ''.join(raw_website).strip() if raw_website else None
                        address = ''.join(raw_address).strip() if raw_address else None

                        business_details = {
                            'no': len(scraped_results),
                            'business_name': business_name,
                            'telephone': telephone,
                            'email': email,
                            'website': website,
                            'address': address,
                            'business_page': business_page
                        }
                        scraped_results.append(business_details)
                    page = page + 1
            elif response.status_code == 404:
                print("Could not find a location matching", place)
                page = 0
                # no need to retry for non existing page
                break
            else:
                print("🔥 Failed to process page. Get in touch with Peter if its not summer!")
                page = 0
                break
        except:
            print("🔥 Failed to process page. Get in touch with Peter!")
            page = 0
            break

    return scraped_results

if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument('keyword', help='Search Keyword - ex: "Precision Grinding"')
    argparser.add_argument('place', help='Place Name - ex: Texas,TX')

    args = argparser.parse_args()
    keyword = args.keyword
    place = args.place
    scraped_data = parse_listing(keyword, place)

    if scraped_data:
        print("💾 Saving data to %s-%s-yellow-data.csv" % (keyword, place))
        with open('%s-%s-yellow-data.csv' % (keyword, place), 'wb') as csvfile:
            fieldnames = ['no', 'business_name', 'telephone', 'email', 'website', 'address', 'business_page']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for data in scraped_data:
                writer.writerow(data)
