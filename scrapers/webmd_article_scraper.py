"""WebMD Article Scraper

This scraper goes through a list of WebMD links and collects the text
in each article. It then breaks the text into sentences and selects 
sentences that contain the words in the SEARCH_TERMS array. 

"""

import re
import time
import csv
import os
import spacy
import getopt, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]
gnuOptions = ["input-file="]

FILE_PATH = ''
SEARCH_TERMS = ['african', 'black']
OUTPUT_FILE = '../data/black_news.csv'

CHROMEDRIVER_PATH = '/Users/Bomani/chromedriver'
WINDOW_SIZE = "1920,1080"

def getDataFromLink(nlp, link):
    relevant_sentences = []
    author_text = 'NONE'

    # Open the page
    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    
    driver = webdriver.Chrome(
        executable_path=CHROMEDRIVER_PATH,
        options=chrome_options
    )  
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

    # Get the authors
    try:
        authors = driver.find_element_by_class_name('authors')
        author_text = authors.text
    except Exception as ex:
        print("Could not get the author.\n\n")
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
    return {'sentences': relevant_sentences, 'authors': author_text}

def getProcessedByline(authors_text):
    authors = authors_text.strip()
    if authors[0:2] == 'By':
        return authors[3:]

def main():
    try:
        arguments, values = getopt.getopt(argument_list, "", gnuOptions)
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))
        sys.exit(2)
    
    # evaluate given options
    for currentArgument, currentValue in arguments:
        if currentArgument in ("--input-file"):
            FILE_PATH = currentValue
            print ("Using search results links from input file:", FILE_PATH)

    nlp = spacy.load("en_core_web_sm")

    previous_links = {}
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if (row[0] in previous_links):
                    previous_links[row[0]] += 1
                else:
                    previous_links[row[0]] = 0

    with open(FILE_PATH) as fp:  
        with open(OUTPUT_FILE, mode = 'a+') as black_file:
            csv_writer = csv.writer(black_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for cnt, link in enumerate(fp):
                if (link in previous_links):
                    print("Skipping link because it has already been scraped: %s. \n" % link)
                    continue
                
                print(link + "\n")
                
                relevant_sents = []

                try:
                    link_data = getDataFromLink(nlp, link)
                    relevant_sents = link_data.get('sentences')
                except Exception as ex:
                    print(ex)
                    continue

                authors = getProcessedByline(link_data.get('authors'))
                for sent in relevant_sents:
                    csv_writer.writerow([link, sent, authors])
                
                time.sleep(2)

                if (cnt % 10 == 0):
                    print("Processed %d links.\n" % cnt)

main()