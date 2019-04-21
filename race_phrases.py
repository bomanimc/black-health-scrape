import re
import time
import csv
import spacy
from selenium import webdriver

FILE_PATH = 'webmd_results.txt'
SEARCH_TERMS = ['african', 'black']
OUTPUT_FILE = 'black.csv'

def getRelevantSentencesFromLink(nlp, link):
    relevant_sentences = []

    # Open the page
    driver = webdriver.Chrome('/Users/Bomani/chromedriver')
    driver.get(link.strip())
    
    # Close the newsletter popup
    try:
        close_popup = driver.find_element_by_id('webmdHoverClose')
        close_popup.click()
    except Exception as ex:
        print("Could not close popup.\n\n")
        print(ex)

    # Click the view all button
    try:
        view_all = driver.find_element_by_class_name('view-all').find_elements_by_css_selector("*")[0]
        view_all.click()
        time.sleep(0.25)
    except Exception as ex:
        print("Could not click View All button.\n\n")
        print(ex)

    # Get all of the article's text
    body = driver.find_element_by_class_name("article-body")
    doc = nlp(body.text)

    # Get the important sentences
    for sent in doc.sents: 
        sent_string = sent.string.strip()
        if any(term in sent_string.lower() for term in SEARCH_TERMS):
            relevant_sentences.append(sent_string)

    driver.close()
    return relevant_sentences


def main():
    nlp = spacy.load("en_core_web_sm")

    previous_links = {}
    with open(OUTPUT_FILE, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if (row[0] in previous_links):
                previous_links[row[0]] += 1
            else:
                previous_links[row[0]] = 0

    with open(FILE_PATH) as fp:  
        with open(OUTPUT_FILE, mode='a') as black_file:
            csv_writer = csv.writer(black_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for cnt, link in enumerate(fp):
                if (link in previous_links):
                    print("Skipping link: %s. \n" % link)
                    continue
                
                print(link + "\n")
                
                try:
                    relevant_sents = getRelevantSentencesFromLink(nlp, link)
                except Exception as ex:
                    print(ex)

                for sent in relevant_sents:
                    csv_writer.writerow([link, sent])
                
                time.sleep(2)

                if (cnt % 10 == 0):
                    print("Processed %d links.\n" % cnt)

main()