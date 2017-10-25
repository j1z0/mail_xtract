import re
import logging
from six.moves.urllib.parse import urlparse

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class EmailSpider(CrawlSpider):
    name = "emails"

    rules = (
        Rule(LinkExtractor(unique=True,
                           deny=(".*\.pdf.*", "utm_content=download")),
             callback='parse_item', follow=True),
    )

    def __init__(self, **kw):
            super(EmailSpider, self).__init__(**kw)
            url = kw.get('url') or kw.get('domain') or 'http://www.jana.com/'
            if not url.startswith('http://') and not url.startswith('https://'):
                url = 'http://%s/' % url
            self.start_urls = [url, ]
            self.allowed_domains = [re.sub(r'^www\.', '', urlparse(url).hostname)]
            self.found = set()

    def parse_item(self, response):

        # seems the deny rule for the linkExtractor doesn't work,
        # so we are still getting pdfs through
        try:
            xselect = scrapy.Selector(response)
            emails = xselect.xpath('//body').re('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+)')
        except AttributeError:
            return

        for email in set(emails):
            if email not in self.found:
                self.found.add(email)
                yield {
                    'email': email
                }
