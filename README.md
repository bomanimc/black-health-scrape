# Black Health Scraper
Online media has likely been the most prominent vector for spreading medical narratives that pathologize Blackness. Statements on Black health often overlook the roles that socioeconomic disparities and anti-Blackness play in health outcomes. They position race as the disease. 

To explore this topic, I built a web scraper to gather hundreds of sentences containing the keywords “black” or “African” from [WebMD](https://www.webmd.com/), one of the most popular online destinations for medical information. Occurrences of these keywords are also present in the articles that WebMD licenses from Health Day, a company that licenses health-related news to major publications.

This repository can be forked and modified to support scraping sentence that match any set of keywords on WebMD.

## Accessing the Dataset
Updated versions of the dataset are published as [releases on this repository](https://github.com/bomanimc/black-health-scraper/releases). You can also use the code in this repository to manually construct the dataset by re-running these scrapers on your own device.

In the future, this dataset will be stored in a database and will be accessible through an API. I also plan to make this scraper run automatically and intermittently so that the dataset grows over time.

## Prerequisites
This project is meant to support Python 3, but is also likely to work correctly with Python 2. 

[Install pipenv](https://github.com/pypa/pipenv#installation) to download the dependencies.
```
brew install pipenv
pipenv install
```

Start the virtual environment containing the downloaded dependencies:
```
pipenv shell
```

[Download a version of Chromedriver](https://chromedriver.chromium.org/downloads) that supports your version of Google Chrome. You can see your version of Chrome by visiting [chrome://settings/help](chrome://settings/help) in the Chrome browser.

## Usage
This project collects sentences from WebMD following a two step process:
1. Use the Search Results Scraper (`search_results.py`) to scrape links to articles that appear in the search results for the query "African American" on WebMD.
2. Use the the Article Sentences Scraper (`article_sents.py`) to visit each search result link collected in the previous step, collect the relevant sentences from each article, and place them into a final output file. 

### Search Results Scraper
To scrape search results for the term "African American" on WebMD, use the following command:

```
python search_results.py --output-folder=path/to/ouput/folder
```

This command will result in the creation of two newline-delimited `.txt` files inside of the specified folder: one containing news article links (those that contain `/news/`) and one containing all other links.

**--output-folder= OR -o**

Optional parameter used for specifying which directory to place the output files into. If the directory doesn't exist, it will be created.

### Article Sentences Scraper
To scrape sentences containing the keywords 'black' or 'african' from WebMD articles, use the following command:

```
python article_sents.py --chromedriver-path=path/to/chromedriver --input-article-links=path/to/search-result-links-file.txt --output-file=path/to/output-file.csv --filter-results
```
This command will result in the creation of a CSV file that contains a collection of sentences matching the keywords. Use of the `--filter-results` flag also means that the results will be filtered to remove potentially irrelevant sentences.

**--chromedriver-path= OR -c**

Required parameter used to specify the path to your Chromedriver binary.

**--input-article-links= OR -i**

Required parameter used to specify the path to the newline-delimited `.txt` file containing the links to the articles that this scraper should evaluated. The simplest approach is to specify a file that was created by the Search Results Scraper.

**--output-file= OR -o**

Optional parameter to specify the path to the CSV file where the results will be stored. If the directory doesn't exist, it will be created. If an output file containing some results is specified, this program will skip links that have already been evaluated. This is a good technique to use if you need to resume scraping after quitting the scraper before it finishes.

**--filter-results OR -f**

Optional flag used to specify that the sentences collected from WebMD articles should be filtered to remove potentially irrelevant sentences based on the logic in `utils/filter_results.py`.
