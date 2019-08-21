# Black Health Scraper
Online media has likely been the most prominent vector for spreading medical narratives that pathologize Blackness. Statements on Black health often overlook the roles that socioeconomic disparities and anti-Blackness play in health outcomes. They position race as the disease. 

To explore this topic, I built a web scraper to gather hundreds of sentences containing the keywords “black” or “African” from [WebMD](https://www.webmd.com/), one of the most popular online destinations for medical information. Occurrences of these keywords are also present in the articles that WebMD licenses from Health Day, a company that licenses health-related news to major publications.

This repository can be forked and modified to support scraping sentence that match any set of keywords on WebMD.

## Prerequisites
[Install pipenv](https://github.com/pypa/pipenv#installation) to download the dependencies.
```
brew install pipenv
pipenv install
```

Start the virtual environment containing the downloaded dependencies:
```
pipenv shell
```

[Download a version of Chromedriver](https://chromedriver.chromium.org/downloads) that supports your version of Google Chrome.