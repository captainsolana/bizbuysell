import asyncio
from bizbuysell_fetch import fetch_listing_urls, fetch_listings, parse_listings, filter_williamson_county_listings, run_listing_calculations, write_listings_to_db_local
from bizbuysell_filter_and_export import filter_objects_and_write_to_csv
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

    if new_listings:
        print(f"Found {len(new_listings)} new listings to fetch")
        asyncio.run(fetch_listings(listing_objs=new_listings, con_limit=con_limit))

        print("Validate listing responses")
        listing_resp_validated = []
        for listing_obj in progressbar(new_listings):
            try:
                if "Soup test failed" not in listing_obj.response_text:
                    listing_resp_validated.append(listing_obj)
            except Exception:
                continue

        if listing_resp_validated:
            parse_listings(listing_resp_validated)
            
            # Filter for Williamson County, TX listings only
            williamson_county_listings = filter_williamson_county_listings(listing_resp_validated)
            
            if williamson_county_listings:
                print("Perform listing calculations")
                for listing_obj in progressbar(williamson_county_listings):
                    financials_present = hasattr(listing_obj, "financials")
                    if financials_present:
                        run_listing_calculations(listing_obj)

                print("Analysis complete.  Write listings to DB")
                write_listings_to_db_local(williamson_county_listings)

                print("Analysis complete.  Write listings to CSV")
                OUTFILE = "/workspaces/bizbuysell/williamson_county_listings.csv"
                filter_objects_and_write_to_csv(williamson_county_listings, OUTFILE)
                print(f"Williamson County listings appended to {OUTFILE}")
            else:
                print("No Williamson County listings found after filtering")
        else:
            print("No valid listings to process after validation")
    else:
        print("No new listings found")
