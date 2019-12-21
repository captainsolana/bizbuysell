import asyncio
from asyncio_pool import AioPool
from bs4 import BeautifulSoup
import csv
import httpx
import json
import os
import pdb
import re
from tenacity import retry, stop_after_attempt


class Serp():
    def __init__(self, *, url, name, formdata):
        self.name = name
        self.firstpage_url = url
        self.formdata = formdata
        self.response_text = ""

    def __repr__(self):
        return self.name


async def fetch_listing_urls(*, con_limit):
    def get_listing_urls_from_response(response_text):

        soup = BeautifulSoup(response_text, "html.parser")
        json_pattern = re.compile(r"SearchResultsPage")
        json_soup = soup.find("script", {"type": "application/ld+json"}, text=json_pattern)
        if json_soup:
            # Quest: it seems like there's got to be a better way to get rid
            # of these characters and make a valid JSON
            json_str = json_soup.contents[0].replace("\r", "").replace("\n", "")
            json_str = json_str.replace("\'", "").replace('\\"', '').replace("\t", "")
            script_dict = json.loads(json_str)
            listing_dicts = script_dict["about"]

            urls = [listing["item"]["url"] for listing in listing_dicts]

            return urls

        return None

    def create_paginated_urls(obj):
        soup = BeautifulSoup(obj.response_text, "html.parser")
        next_page_present = True if soup.find("a", {"title": "Next"}) else False
        if next_page_present:
            next_page_soup = soup.find("a", {"title": "Next"})

            # Navigate to the element before to find the number of the last page
            num_of_pages = int(next_page_soup.parent.previous_sibling.text)

            # Example paginated url
            # https://www.bizbuysell.com/florida/automotive-and-boat-businesses-for-sale/3/
            paginated_urls = [f"{obj.firstpage_url}/{i}" for i in range(2, num_of_pages + 1)]

            return paginated_urls

    @retry(stop=stop_after_attempt(5))
    async def fetch_url(url):
        SCRAPER_API_KEY = os.environ.get('SCRAPER_API_KEY', '')
        SCRAPERAPI_URL = 'http://api.scraperapi.com'

        param_payload = {
            'api_key': SCRAPER_API_KEY,
            'url': url,
        }

        async with httpx.AsyncClient() as client:
            print(f"Trying #{paginated_url_list.index(url)}")
            r = await client.get(SCRAPERAPI_URL, params=param_payload, timeout=60)
            test_soup = BeautifulSoup(r.text, 'html.parser')
            if test_soup.find("h1", {"class": "search-result-h1"}):
                print(f"{paginated_url_list.index(url)} complete!")
                return r.text
            else:
                obj.response_text = "Soup test failed"
                raise ValueError(f"Soup test failed for #{paginated_url_list.index(url)}")

    async def fetch_obj_with_url(obj):
        SCRAPER_API_KEY = os.environ.get('SCRAPER_API_KEY', '')
        SCRAPERAPI_URL = 'http://api.scraperapi.com'

        param_payload = {
            'api_key': SCRAPER_API_KEY,
            'url': obj.firstpage_url,
        }

        async with httpx.AsyncClient() as client:
            print(f"Trying {obj.name}")
            r = await client.get(SCRAPERAPI_URL, params=param_payload, timeout=60)
            test_soup = BeautifulSoup(r.text, 'html.parser')
            if test_soup.find("h1", {"class": "search-result-h1"}):
                obj.response_text = r.text
                print(f"{obj.name} complete!")
            else:
                obj.response_text = "Soup test failed"
                raise ValueError(f"Soup test failed for {obj.name}")

    def generate_serp_objs():
        # x=1 hides listing with no asking price.
        # hb=h hides home based businesses

        states = {
            "AK": "Alaska",
            "AL": "Alabama",
            "AR": "Arkansas",
            "AZ": "Arizona",
            "CA": "California",
            "CO": "Colorado",
            "CT": "Connecticut",
            "DE": "Delaware",
            "FL": "Florida",
            "GA": "Georgia",
            "HI": "Hawaii",
            "IA": "Iowa",
            "ID": "Idaho",
            "IL": "Illinois",
            "IN": "Indiana",
            "KS": "Kansas",
            "KY": "Kentucky",
            "LA": "Louisiana",
            "MA": "Massachusetts",
            "MD": "Maryland",
            "ME": "Maine",
            "MI": "Michigan",
            "MN": "Minnesota",
            "MO": "Missouri",
            "MS": "Mississippi",
            "MT": "Montana",
            "NC": "North Carolina",
            "ND": "North Dakota",
            "NE": "Nebraska",
            "NH": "New Hampshire",
            "NJ": "New Jersey",
            "NM": "New Mexico",
            "NV": "Nevada",
            "NY": "New York",
            "OH": "Ohio",
            "OK": "Oklahoma",
            "OR": "Oregon",
            "PA": "Pennsylvania",
            "RI": "Rhode Island",
            "SC": "South Carolina",
            "SD": "South Dakota",
            "TN": "Tennessee",
            "TX": "Texas",
            "UT": "Utah",
            "VA": "Virginia",
            "VT": "Vermont",
            "WA": "Washington",
            "WI": "Wisconsin",
            "WV": "West Virginia",
            "WY": "Wyoming"
        }

        data_objects = []
        for state in states:
            for category in categories:
                # Example URL
                # https://www.bizbuysell.com/florida/restaurants-and-food-businesses-for-sale

                base_url = "https://www.bizbuysell.com"
                companies_str = "businesses-for-sale"

                serp_object = Serp(
                    formdata={"x": 1, "s": state, "i": categories[category]},
                    name=f"{state}-{category.replace(' ', '_')}",
                    url=f"{base_url}/{states[state]}/{category}-{companies_str}"
                )
                data_objects.append(serp_object)

        return data_objects

    with open("category_arguments.csv", mode="r", encoding="utf-8-sig") as csv_file:
        reader = csv.reader(csv_file)
        categories = {rows[0]: rows[1] for rows in reader}
        del categories["name"]

    data_objects = generate_serp_objs()
    data_objects = data_objects[155:160]

    print(f"{len(data_objects)} categories to process")
    pool = AioPool(size=con_limit)
    await pool.map(fetch_obj_with_url, data_objects)

    paginated_url_list = []
    for obj in data_objects:
        paginated_urls = create_paginated_urls(obj)
        if paginated_urls:
            paginated_url_list.extend(paginated_urls)

    paginated_url_response_list = await pool.map(fetch_url, paginated_url_list)

    serp_response_list = [obj.response_text for obj in data_objects]
    serp_response_list.extend(paginated_url_response_list)

    # Get Listing URLs
    listing_urls = []
    for serp_response in serp_response_list:
        listing_url_holding = get_listing_urls_from_response(serp_response)
        if listing_url_holding:
            listing_urls.extend(listing_url_holding)

    pdb.set_trace()


if __name__ == "__main__":
    asyncio.run(fetch_listing_urls(con_limit=10))
