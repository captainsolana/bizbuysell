import asyncio
from bs4 import BeautifulSoup
import csv
import httpx
import os
import pdb
import pickle
from tenacity import retry, stop_after_attempt


class Serp():
    def __init__(self, *, formdata, name):
        self.formdata = formdata
        self.name = name

    def __repr__(self):
        return self.name


def async_fetch(*, object_list, con_limit, out_file):
    '''
    Objects must have url parameter to work
    '''
    @retry(stop=stop_after_attempt(5))
    async def fetch(myobject):
        SCRAPER_API_KEY = os.environ.get('SCRAPER_API_KEY', '')
        SCRAPERAPI_URL = 'http://api.scraperapi.com'

        post_url = f"https://www.bizbuysell.com/listings/handlers/searchresultsredirector.ashx"

        param_payload = {
            'api_key': SCRAPER_API_KEY,
            'url': post_url,
        }

        data_payload = myobject.formdata

        async with httpx.AsyncClient() as client:
            r = await client.post(SCRAPERAPI_URL, data=data_payload, params=param_payload, timeout=60)
            test_soup = BeautifulSoup(r.text, 'html.parser')
            if test_soup.find("h1", {"class": "search-result-h1"}):
                myobject.response_text = r.text
            else:
                myobject.response_text = 'Soup test failed'
                raise ValueError(f'Soup test failed for {myobject.name}')

    async def fetch_with_limits(object_list):
        dltasks = set()
        for myobject in object_list:
            try:
                if len(dltasks) >= con_limit:
                    # Wait for a download to finish before adding a new one
                    _done, dltasks = await asyncio.wait(dltasks, return_when=asyncio.FIRST_COMPLETED)  # noqa
                dltasks.add(asyncio.create_task(fetch(myobject)))
            except Exception as e:
                print(f'Continuing. The problem was {e}')
                break
        # Wait for the remaining downloads to finish
        await asyncio.wait(dltasks)

    def save_object(obj, filename):
        with open(filename, 'wb') as output:  # Overwrites any existing file.
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

    asyncio.run(fetch_with_limits(object_list))
    pdb.set_trace()
    save_object(object_list, out_file)


def main():
    def generate_serp_posts():
        # x=1 hides listing with no asking price.
        # hb=h hides home based businesses

        states = {
            'AK': 'Alaska',
            'AL': 'Alabama',
            'AR': 'Arkansas',
            'AS': 'American Samoa',
            'AZ': 'Arizona',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DC': 'District of Columbia',
            'DE': 'Delaware',
            'FL': 'Florida',
            'GA': 'Georgia',
            'GU': 'Guam',
            'HI': 'Hawaii',
            'IA': 'Iowa',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'MA': 'Massachusetts',
            'MD': 'Maryland',
            'ME': 'Maine',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MO': 'Missouri',
            'MP': 'Northern Mariana Islands',
            'MS': 'Mississippi',
            'MT': 'Montana',
            'NA': 'National',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'NE': 'Nebraska',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NV': 'Nevada',
            'NY': 'New York',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'PR': 'Puerto Rico',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VA': 'Virginia',
            'VI': 'Virgin Islands',
            'VT': 'Vermont',
            'WA': 'Washington',
            'WI': 'Wisconsin',
            'WV': 'West Virginia',
            'WY': 'Wyoming'
        }

        data_objects = []
        for state in states:
            for category in categories:
                data_objects.append(Serp(formdata={"x": 1, "s": state, "i": category}, name=f"{state}-{category}"))

        return data_objects

    with open("category_arguments.csv", mode="r", encoding="utf-8-sig") as csv_file:
        reader = csv.reader(csv_file)
        categories = {rows[0]: rows[1] for rows in reader}
        del categories["Normal Name"]

    data_objects = generate_serp_posts()
    outfile = "/Users/work/Desktop/bizbuysell_data/serp_responses.pkl"
    async_fetch(object_list=data_objects[:2], con_limit=250, out_file=outfile)


if __name__ == "__main__":
    main()
