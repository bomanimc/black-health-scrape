import re
import time
import spacy
from requests_html import HTMLSession

FILE_PATH = 'webmd_results.txt'
SEARCH_TERM = 'african'

def main():
    session = HTMLSession()
    nlp = spacy.load("en_core_web_sm")

    lines_of_interest = []

    with open(FILE_PATH) as fp:  
        for cnt, line in enumerate(fp):
            print(line + "\n")
            
            resp = session.get(line.strip())
            resp.html.render()
            article_p = resp.html.find('p')

            for p in article_p:
                print(p)
                print(p.text)
                doc = nlp(p.text)
                print(list(doc.sents))
                lines_of_interest += list(doc.sents)

            time.sleep(5)

            if (cnt > 50):
                break
            
            break

    print(lines_of_interest)

main()