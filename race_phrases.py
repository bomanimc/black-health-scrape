import re
import time
from requests_html import HTMLSession

FILE_PATH = 'webmd_results.txt'
SEARCH_TERM = 'african'

def main():
    session = HTMLSession()

    lines_of_interest = []

    with open(FILE_PATH) as fp:  
        for cnt, line in enumerate(fp):
            print(line + "\n")
            
            resp = session.get(line.strip())
            resp.html.render()
            article_p = resp.html.find('p')

            for p in article_p:
                # TODO: Us a better approach for splittng the string into sentences
                sentences = re.findall(r"([^.]*?%s[^.]*\.)" % SEARCH_TERM, p.text.lower())
                print(sentences);
                lines_of_interest += sentences

            time.sleep(5)

            if (cnt > 50):
                break;
            

    print(lines_of_interest)

main()