# Big Structure

For the initial scrape
- [x] Get starting SERP urls
- [x] Get listing urls
- [x] Fetch listings

For updates
- [x] Get SERPs (use functions from initial fetch)
- [x] Check listing URLs against our db
- [x] Fetch listings that aren't in the db

For removed listings
- [] Check documents for ```date_last_not_seen``` flag
- [] If not present, get listing url responses
- [] Check response for "doesn't exist" string 

# Setting it up to run regularly
https://www.maketecheasier.com/use-launchd-run-scripts-on-schedule-macos/

First, I bash command is needed:
```/Users/work/Dropbox/bash-scripts/landwatchquantitybash.sh```
Second a plist command is needed
```~/Library/LaunchAgents/local.work.bizbuysell.plist```
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