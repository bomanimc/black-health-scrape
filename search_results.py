import getopt
import sys
import datetime
from scrapers import webmd_search_results_scraper

write_time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

# Default Configurations
OUTPUT_FOLDER_PATH = 'data/test/search_result_links_' + write_time

full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]
gnuOptions = ['output-folder=']

try:
    arguments, values = getopt.getopt(argument_list, "", gnuOptions)
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))
    sys.exit(2)

for currentArgument, currentValue in arguments:
    if currentArgument in ("--output-folder"):
        OUTPUT_FOLDER_PATH = currentValue

def validateConfigValues():
    if (OUTPUT_FOLDER_PATH == None):
        sys.exit(2)

def main():
    validateConfigValues()
    webmd_search_results_scraper.scrape_search_result_links(OUTPUT_FOLDER_PATH)

main()
