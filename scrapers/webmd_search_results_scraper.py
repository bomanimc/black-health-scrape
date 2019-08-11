"""WebMD Search Results Scraper

This scraper is used to scrape a list of links that are returned when 
"African American" is searched on WebMD. These links are compiled
line-by-line into a .txt file file.

"""

import os
import datetime
from requests_html import HTMLSession

BASE_SEARCH_URL = 'https://www.webmd.com/search/search_results/default.aspx?query=african%20american&page='

def main():
    session = HTMLSession()
    status_code = 200
    pagination_counter = 1

    write_time = datetime.datetime.now()
    filename = "../data/webmd_search_results/webmd_search_results_" + str(write_time) + ".txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, "w+") as f:
        while (status_code == 200):
            resp = session.get(BASE_SEARCH_URL + str(pagination_counter))
            status_code = resp.status_code
            results = resp.html.find('.results-container', first=True)
            
            if (results == None):
                print("Ended link scraping on results page %d.\n" % (pagination_counter - 1))
                break

            for _, link in enumerate(results.absolute_links):
                f.write(link + "\n")

            if (pagination_counter % 10 == 0):
                print("Added links up to results page %d.\n" % pagination_counter)
            
            pagination_counter += 1

        f.close()

main()
