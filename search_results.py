import click
import datetime
from scrapers import webmd_search_results_scraper

write_time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

@click.command()
@click.option(
    '-o', '--output-folder', 'output_folder',
    default = 'data/test/search_result_links_' + write_time,
    show_default = True,
    help = """Used for specifying which directory to place the 
    output files into. If the directory doesn't exist, it will be created."""
)
def main(output_folder):
    webmd_search_results_scraper.scrape_search_result_links(output_folder)

if __name__ == '__main__':
    main()