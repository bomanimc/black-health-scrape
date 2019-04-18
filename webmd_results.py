from requests_html import HTMLSession

BASE_SEARCH_URL = 'https://www.webmd.com/search/search_results/default.aspx?query=african%20american&page='

def main():
    session = HTMLSession()
    status_code = 200
    pagination_counter = 1

    f = open("webmd_results.txt","w+")

    while (status_code == 200):
        pagination_counter += 1
        resp = session.get(BASE_SEARCH_URL + str(pagination_counter))
        status_code = resp.status_code
        results = resp.html.find('.results-container', first=True)
        
        if (results == None):
            break;

        for _, link in enumerate(results.absolute_links):
            f.write(link + "\n")

        if (pagination_counter % 10 == 0):
            print("Added links up to results page %d.\n" % pagination_counter)
        
    f.close()

main()
