#!/usr/bin/env python3
"""
Test script to verify Williamson County filtering logic
"""

import asyncio
from bizbuysell_fetch import fetch_listing_urls, fetch_listings, parse_listings, filter_williamson_county_listings

def test_williamson_filter():
    """Test the Williamson County filter with mock data"""
    
    # Create mock listing objects to test the filter
    class MockListing:
        def __init__(self, custom_name, address):
            self.custom_name = custom_name
            self.address = address
    
    test_listings = [
        MockListing("test1", {"addressLocality": "Round Rock", "addressRegion": "TX"}),
        MockListing("test2", {"addressLocality": "Austin", "addressRegion": "TX"}),
        MockListing("test3", {"addressLocality": "Cedar Park", "addressRegion": "TX"}),
        MockListing("test4", {"addressLocality": "Dallas", "addressRegion": "TX"}),
        MockListing("test5", {"addressLocality": "Georgetown", "addressRegion": "TX"}),
        MockListing("test6", "Round Rock, TX"),
        MockListing("test7", "Cedar Park, Williamson County, TX"),
        MockListing("test8", "Houston, TX"),
    ]
    
    print("Testing Williamson County filter with mock data:")
    print(f"Total test listings: {len(test_listings)}")
    
    # Test the filter
    williamson_listings = filter_williamson_county_listings(test_listings)
    
    print(f"Filtered results: {len(williamson_listings)} Williamson County listings found")
    for listing in williamson_listings:
        print(f"  - {listing.custom_name}: {listing.address}")

if __name__ == "__main__":
    test_williamson_filter()
