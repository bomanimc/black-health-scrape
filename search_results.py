import click
import datetime
from scrapers import webmd_search_results_scraper

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

write_time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    '-o', '--output-folder', 'output_folder',
    default = 'data/test/search_result_links_' + write_time,
    show_default = True,
    help = (
        f"Used for specifying which directory to place the output files "
        f"into. If the directory doesn't exist, it will be created."
    )
)
def main(output_folder):
    webmd_search_results_scraper.scrape_search_result_links(output_folder)

if __name__ == '__main__':
    main()