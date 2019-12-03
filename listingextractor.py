import pdb
import extruct
import requests
from bs4 import BeautifulSoup
from w3lib.html import get_base_url


class Business:
    def __init__(self, *, values, keys, name):
        self.__dict__ = dict(zip(keys, values))
        self.name = name


sample_data = {
    'Date Retrieved': '10/15/2019',
    'ListingURL': 'https://bizbuysell.com/Business-Opportunity/Arizona-Glass-Contractor/1567381/',
    'Asking Price': 5750000,
    'Cash Flow': 1800000,
    'Gross Revenue': 17000000,
    'EBITDA': 1600000,
    'FF&E': 500000,
    'Inventory': 'N/A',
    'Rent': '$14,500/Month',
    'Established': 1985,
    'Location': 'Phoenix, AZ',
    'Real Estate': 'Leased',
    'Building SF': 33000,
    'Lease Expiration': '12/31/2021',
    'Employees': 90,
    'Furniture, Fixtures, & Equipment (FF&E)': 'Included in asking price',
    'Facilities': '33,000 square feet of office and warehouse',
    'Competition': 'Over the past few years, the metropolitan Phoenix area has increased its population by more than 10% annually; accordingly, construction spending has been strong.',
    'Support & Training': 'Management team in place. Owner will assist with transition as needed.',
    'Reason for Selling': 'Retirement'
}

r = requests.get('https://www.bizbuysell.com/Business-Opportunity/Flowers-Bread-Route-Mesa-AZ/1685235/')
soup = BeautifulSoup(r.content, 'html.parser')
base_url = get_base_url(r.text, r.url)
data = extruct.extract(r.text, base_url=base_url)

pdb.set_trace()
