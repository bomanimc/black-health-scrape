"""WebMD Search Results Scraper

This scraper is used to scrape a list of links that are returned when 
"African American" is searched on WebMD. These links are compiled
line-by-line into a .txt file file.

"""

import os
import pandas as pd
from requests_html import HTMLSession

BASE_SEARCH_URL = 'https://www.webmd.com/search/search_results/default.aspx?query=african%20american&page='

def scrape_search_result_links(output_folder_path):
    session = HTMLSession()
    status_code = 200
    pagination_counter = 1
    search_result_links = []

    while (status_code == 200):
        resp = session.get(BASE_SEARCH_URL + str(pagination_counter))
        status_code = resp.status_code
        results = resp.html.find('.results-container', first = True)
        
        if (results == None):
            print("Ended link scraping on results page %d.\n" % (pagination_counter - 1))
            break
        
        for _, link in enumerate(results.absolute_links):
            search_result_links.append(link)

        if (pagination_counter % 10 == 0):
            print("Added links up to results page %d.\n" % pagination_counter)
        
        pagination_counter += 1

    os.makedirs(os.path.dirname(output_folder_path), exist_ok=True)

    search_result_df = pd.DataFrame(search_result_links, columns=['search_result_url'])
    search_result_df.to_csv(output_folder_path + '.csv', index=False)
