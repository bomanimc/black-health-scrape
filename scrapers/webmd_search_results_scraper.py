"""WebMD Search Results Scraper

This scraper is used to scrape a list of links that are returned when 
"African American" is searched on WebMD. These links are compiled
line-by-line into a .txt file file.

"""

import os
from requests_html import HTMLSession

BASE_SEARCH_URL = 'https://www.webmd.com/search/search_results/default.aspx?query=african%20american&page='

def scrape_search_result_links(output_folder_path):
    session = HTMLSession()
    status_code = 200
    pagination_counter = 1

    news_links_filename = output_folder_path + "/news_search_results.txt"
    other_links_filename = output_folder_path + "/other_search_results.txt"
    os.makedirs(os.path.dirname(news_links_filename), exist_ok=True)
    os.makedirs(os.path.dirname(other_links_filename), exist_ok=True)
    
    with open(news_links_filename, "w+") as news_file:
        with open(other_links_filename, "w+") as other_file:
            while (status_code == 200):
                resp = session.get(BASE_SEARCH_URL + str(pagination_counter))
                status_code = resp.status_code
                results = resp.html.find('.results-container', first=True)
                
                if (results == None):
                    print("Ended link scraping on results page %d.\n" % (pagination_counter - 1))
                    break

                for _, link in enumerate(results.absolute_links):
                    if ('/news/' not in link):
                        other_file.write(link + "\n")
                    else:
                        news_file.write(link + "\n") 

                if (pagination_counter % 10 == 0):
                    print("Added links up to results page %d.\n" % pagination_counter)
                
                pagination_counter += 1

            news_file.close()
            other_file.close()
