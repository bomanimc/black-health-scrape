import click
import datetime
from scrapers import webmd_article_scraper

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

write_time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    '-c', '--chromedriver-path', 'chromedriver_path',
    default = None,
    required = True,
    help = "Used to specify the path to your Chromedriver binary."
)
@click.option(
    '-i', '--input-articles-file', 'input_articles_file',
    default = None,
    required = True,
    help = (
        f"Used to specify the path to the newline-delimited .txt file containing the "
        f"links to the articles that this scraper should evaluated. The simplest " 
        f"approach is to specify a file that was created by the Search Results Scraper."
    )
)
@click.option(
    '-o', '--output-file', 'output_file',
    default = 'data/test/webmd_sentences/article_sents_' + write_time + '.csv',
    show_default = True,
    help = (
        f"Used to specify the path to the CSV file where the results will be stored. " 
        f"If the directory doesn't exist, it will be created. If an output file "
        f"containing some results is specified, this program will skip links that "
        f"have already been evaluated. This is a good technique to use if you need "
        f"to resume scraping after quitting the scraper before it finishes."
    )
)
@click.option(
    '-f', '--filter-results', 'should_filter_results',
    default = False,
    show_default = True,
    is_flag=True,
    help = (
        f"Used to specify that the sentences collected from WebMD articles should be "
        f"filtered to remove potentially irrelevant sentences based on the logic in "
        f"utils/filter_results.py."
    )
)
def main(chromedriver_path, input_articles_file, output_file, should_filter_results):
    webmd_article_scraper.scrape_sents(
        input_articles_file,
        output_file,
        chromedriver_path,
        should_filter_results
    )

if __name__ == '__main__':
    main()
