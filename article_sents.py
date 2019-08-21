import getopt
import sys
import datetime
from scrapers import webmd_article_scraper

write_time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

# Default Configurations
OUTPUT_FILE_NAME = 'data/test/webmd_sentences/article_sents_' + write_time + '.csv'
SHOULD_FILTER_RESULTS = False
RESUME_FILE = None
INPUT_ARTICLE_LINKS_FILE = None
CHROMEDRIVER_PATH = None

full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]
gnuOptions = [
    'chromedriver-path=', 
    'input-articles-file=',
    'output-file=',
    'filter-results'
]

try:
    arguments, values = getopt.getopt(argument_list, "", gnuOptions)
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))
    sys.exit(2)

for currentArgument, currentValue in arguments:
    if currentArgument in ("--chromedriver-path"):
        CHROMEDRIVER_PATH = currentValue
    elif currentArgument in ("--input-articles-file"):
        INPUT_ARTICLE_LINKS_FILE = currentValue
        print("Using search results links from input file:", INPUT_ARTICLE_LINKS_FILE)
    elif currentArgument in ("--output-file"):
        OUTPUT_FILE_NAME = currentValue
    elif currentArgument in ("--filter-results"):
        SHOULD_FILTER_RESULTS = True

def printConfigurationValues():
    print("OUTPUT_FILE_NAME", OUTPUT_FILE_NAME)
    print("SHOULD_FILTER_RESULTS", SHOULD_FILTER_RESULTS)
    print("INPUT_ARTICLE_LINKS_FILE", INPUT_ARTICLE_LINKS_FILE)
    print("CHROMEDRIVER_PATH", CHROMEDRIVER_PATH)

def validateConfigValues():
    if (INPUT_ARTICLE_LINKS_FILE == None or CHROMEDRIVER_PATH == None):
        if (INPUT_ARTICLE_LINKS_FILE == None):
            print ("Must provide filename for input articles file path.")
        elif (CHROMEDRIVER_PATH == None):
            print ("Must set Chromedriver path.")

        sys.exit(2)

def main():
    validateConfigValues()

    webmd_article_scraper.scrape_sents(
        INPUT_ARTICLE_LINKS_FILE,
        OUTPUT_FILE_NAME,
        CHROMEDRIVER_PATH,
        SHOULD_FILTER_RESULTS
    )

main()
