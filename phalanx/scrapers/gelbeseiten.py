import re
import logging
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

from phalanx.scrapers.config import (
    BASE_URLS, HEADERS,
    REQUEST_TIMEOUT, MAX_RETRIES, REQUEST_DELAY
)

class GelbeSeitenScraper:
    """
    A scraper for extracting business information from GelbeSeiten.
    """

    BASE_URL = BASE_URLS.get("gelbeseiten", "https://www.gelbeseiten.de")

    def __init__(self, search_query, location="bundesweit"):
        """
        Initialize the scraper with a search query and location.

        :param search_query: The type of business or service to search for.
        :param location: The location to search in.
        """
        self.search_query = search_query
        self.location = location
        self.session = requests.Session()
        self.headers = HEADERS
        self.timeout = REQUEST_TIMEOUT
        self.max_retries = MAX_RETRIES
        self.request_delay = REQUEST_DELAY

    def build_search_url(self):
        """
        Build the search URL based on the query and location.

        :return: The complete search URL.
        """
        return f"{self.BASE_URL}/suche/{self.search_query}/{self.location}"

    def fetch_page(self, url):
        """
        Fetch the HTML content of a page.

        :param url: The URL to fetch.
        :return: The HTML content of the page.
        """
        try:
            response = self.session.get(url, headers=self.headers, timeout=self.timeout, )
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error("Error fetching URL %s: %s", url, e)
            return None

    def __process_business_listings(self, urls: List[str]) -> List[Dict[str, str]]:
        
        business_info = []
        
        for url in urls:
            business_page = self.fetch_page(url)
            soup = BeautifulSoup(business_page, 'html.parser')
            # Extract business name
            business_name = soup.select_one(".mod-TeilnehmerKopf__name")
            business_name = business_name.text.strip() if business_name else None

            # Extract email
            email_element = soup.find(id='email_versenden')
            email = None
            
            if email_element and email_element.has_attr('data-link'):
                email_match = re.search(r'mailto:([^?]+)', email_element['data-link'])
                email = email_match.group(1) if email_match else None
            
            # Extract address
            address = soup.find('address')
            address = address.text.strip() if address else None

            # Extract address from "mod-TeilnehmerKopf__adresse" class
            additional_address = soup.find('div', class_='mod-TeilnehmerKopf__adresse')
            additional_address = additional_address.text.strip() if additional_address else None

            # Extract phone number
            phone = soup.find('span', {'data-role': 'telefonnummer'})
            phone = phone.text.strip() if phone else None

            # Extract website
            website_element = soup.select_one('div.aktionsleiste-button a[href]')
            website = website_element['href'] if website_element else None

            
            # Extract further information
            further_info = soup.select_one('.mod-ZusatzInhalte')
            further_info = further_info.text.strip() if further_info else None
            
            # Extract raw contact information
            raw_contact_info = soup.select_one('#kontaktdaten')
            raw_contact_info = raw_contact_info.text.strip() if raw_contact_info else None
            
            # Extract raw company information
            raw_company_info = soup.select_one('#beschreibung')
            raw_company_info = raw_company_info.text.strip() if raw_company_info else None
            
            
            business_info.append({
                'business_name': business_name,
                'address': address or additional_address,
                'phone': phone,
                'email': email,
                'website': website,
                'further_info': further_info,
                'raw_contact_info': raw_contact_info,
                'raw_company_info': raw_company_info,
            })

        return business_info
        
    def __parse_business_listings(self, html_content):
        """
        Parse the HTML content to extract business listings.

        :param html_content: The HTML content of the page.
        :return: A list of dictionaries containing business information.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        listings: List[str] = []

        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.startswith(f"{self.BASE_URL}/gsbiz"):
                listings.append(href)

        return self.__process_business_listings(listings)

    def scrape(self):
        """
        Perform the scraping process.

        :return: A list of business listings.
        """
        search_url = self.build_search_url()
        html_content = self.fetch_page(search_url)

        if not html_content:
            logging.error("Failed to fetch the search results page.")
            return []

        return self.__parse_business_listings(html_content)


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Example usage
    sq = "bauunternehmen"
    lctn = "bundesweit"

    scraper = GelbeSeitenScraper(sq, lctn)
    results = scraper.scrape()

    for idx, business in enumerate(results, start=1):
        print(f"{idx}. {business['business_name']}")
        print(f"   Address: {business['address']}")
        print(f"   Phone: {business['phone']}")
        print(f"   Website: {business['website']}")
        print(f"   Email: {business['email']}")
        print()