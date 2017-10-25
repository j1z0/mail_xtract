import argparse
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def getargs():
    parser = argparse.ArgumentParser(
        description="Scrape a domain for all email addresses",
        )
    parser.add_argument('domain')
    parser.add_argument('-log', action='store_true', default=False)

    return parser.parse_args()


def main(args):
    if not args.log:
        logging.getLogger('scrapy').propagate = False

    settings = get_project_settings()
    process = CrawlerProcess(settings)

    process.crawl('emails', domain=args.domain)

    print("Found these email addresses:")
    process.start()


if __name__ == "__main__":
    main(getargs())
