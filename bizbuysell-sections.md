# Search
POST to https://www.bizbuysell.com/listings/handlers/searchresultsredirector.ashx
Example CURL https://termbin.com/1mng

i = Category
s = State abbreviation (use as many as you want).  E.g. AL or MI
x = 1 <= Hide listings without a price
hb = h Hide home-based


# Listing
3 sections

1) the big JSON
2) header spot (class="span12").  Turn this into a dictionary
    - soup.find(text=re.compile('Asking Price')).parent.parent.parent.parent.parent.text
3) listing details (class="listingProfile_details")
    - soup.find_all("div", class_="listingProfile_details")