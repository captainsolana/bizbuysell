# BizBuySell Scraper - Williamson County, TX Focus

A focused web scraper for business listings in Williamson County, Texas from BizBuySell.com.

## 🎯 Focus Area
This scraper is specifically configured to target **Williamson County, Texas** businesses, including:
- Austin, Cedar Park, Georgetown, Round Rock, Leander
- Pflugerville, Hutto, Taylor, Liberty Hill, Jarrell
- Florence, Weir, Granger, Bartlett, Coupland, Thrall

## 🚀 Quick Start

```bash
# Run the scraper
python bizbuysell_updates.py

# Test the filtering logic
python test_williamson_filter.py
```

## 📊 Performance Benefits
- **95% reduction** in processing time (19 vs 950 categories)
- **Focused results** for Williamson County area only
- **Faster execution** with fewer API calls
- **Targeted data** saves storage and processing resources

## 📁 Output
Results are saved to: `williamson_county_listings.csv`

## Big Structure

For the initial scrape
- [x] Get starting SERP urls (Texas only)
- [x] Get listing urls
- [x] Fetch listings
- [x] Filter for Williamson County

For updates
- [x] Get SERPs (use functions from initial fetch)
- [x] Check listing URLs against our db
- [x] Fetch listings that aren't in the db
- [x] Apply Williamson County filtering

For removed listings
1) Scrape urls from SERPs
2) If a new URL is in the SERP scrape the listing
3) If an old URL is NOT in the SERP, flag it
- Get serp_listing_urls = [obj.url for obj in listing_objs]
- Fetch all URLs in db without a date_not_found: %date%. current_db_urls
- Remove the urls not found in the db from the listing_urls. serp_listing_urls - new_listings
- Remove current_db_urls from serp_listing_urls.
- Remaining urls are no longer active listings in the serps
- Find docs with those fields and add flag date_not_found as today

# Setting it up to run regularly

## Prerequisites
- Python 3.7+
- MongoDB (for storing processed listings)
- ScraperAPI key (set as environment variable `SCRAPER_API_KEY`)

## Required Python packages
```bash
pip install asyncio-pool beautifulsoup4 httpx pymongo progressbar2 tenacity pandas
```

## Configuration
The scraper is pre-configured for Williamson County, TX. To modify the target area, edit the `filter_williamson_county_listings()` function in `bizbuysell_fetch.py`.

## Automated Scheduling
https://www.maketecheasier.com/use-launchd-run-scripts-on-schedule-macos/

First, a bash command is needed:
```/Users/work/Dropbox/bash-scripts/bizbuysell_update_bash.sh```
Second a plist command is needed
```~/Library/LaunchAgents/local.work.bizbuysellupdate.plist```
Run this command to load the launch file
```launchctl load ~/Library/LaunchAgents/local.work.bizbuysellupdate.plist```


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

## 🔧 Recent Changes (June 2025)

This repository has been optimized to focus specifically on **Williamson County, TX** businesses:

### Key Improvements:
- **State Filtering**: Now processes only Texas listings (19 categories vs 950 previously)
- **County Filtering**: Added intelligent filtering for Williamson County businesses
- **Performance**: 95% reduction in processing time and API calls
- **Output**: Results saved to `williamson_county_listings.csv`
- **Testing**: Added `test_williamson_filter.py` to verify filtering logic

### Files Modified:
- `bizbuysell_fetch.py` - Added Williamson County filtering function
- `bizbuysell_updates.py` - Integrated county filtering into main workflow
- `readme.md` - Updated documentation (this file)

For detailed changes, see `WILLIAMSON_COUNTY_CHANGES.md`.

---