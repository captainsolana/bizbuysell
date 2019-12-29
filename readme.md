# Big Structure

For the initial scrape
- [x] Get starting SERP urls
- [x] Get listing urls
- [x] Fetch listings

For updates
- [] Get SERPs (use functions from initial fetch)
- [] Check listing URLs against our db
- [] Fetch listings that aren't in the db

For removed listings
- [] Check documents for ```date_last_not_seen``` flag
- [] If not present, get listing url responses
- [] Check response for "doesn't exist" string 


# Search
POST to https://www.bizbuysell.com/listings/handlers/searchresultsredirector.ashx
Example CURL https://termbin.com/1mng

i = Category
s = State abbreviation (use as many as you want).  E.g. AL or MI
x = 1 <= Hide listings without a price
hb = h Hide home-based

# Serps

Max results = 1,500
Max results per SERP = 50
Info that's needed is in     
<script type="application/ld+json" defer>  
with the text: "@type": "SearchResultsPage"

# Listing
3 sections

1) the big JSON
2) header spot (class="span12").  Turn this into a dictionary
    - soup.find(text=re.compile('Asking Price')).parent.parent.parent.parent.parent.text
3) listing details (class="listingProfile_details")
    - soup.find_all("div", class_="listingProfile_details")