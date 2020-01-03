import asyncio
from bizbuysell_fetch import fetch_listing_urls, fetch_listings, parse_listings, run_listing_calculations, write_listings_to_db_local
from progressbar import progressbar
import pymongo


def check_if_urls_in_db(listing_objs):
    MONGO_URI = "mongodb://127.0.0.1:27017/"
    client = pymongo.MongoClient(MONGO_URI)
    db = client["bizbuysell"]
    collection = db["listings"]

    listings_not_in_db = []
    for obj in progressbar(listing_objs):
        if collection.count_documents({"url": obj.url}) == 0:
            listings_not_in_db.append(obj)

    return listings_not_in_db


if __name__ == "__main__":
    con_limit = 25
    listing_objs = asyncio.run(fetch_listing_urls(con_limit=con_limit))

    print("Check if listing is in db")
    new_listings = check_if_urls_in_db(listing_objs)

    asyncio.run(fetch_listings(listing_objs=new_listings, con_limit=con_limit))

    print("Validate listing responses")
    listing_resp_validated = []
    for listing_obj in progressbar(listing_objs):
        try:
            if "Soup test failed" not in listing_obj.response_text:
                listing_resp_validated.append(listing_obj)
        except Exception:
            continue

    parse_listings(listing_resp_validated)

    print("Perform listing calculations")
    for listing_obj in progressbar(listing_resp_validated):
        financials_present = hasattr(listing_obj, "financials")
        if financials_present:
            run_listing_calculations(listing_obj)

    print("Analysis complete.  Write listings to DB")
    write_listings_to_db_local(listing_objs)
