# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class EmailxtractPipeline(object):
    seen_email = set()

    def process_item(self, item, spider):
        email = item.get('email')
        if email not in self.seen_email:
            print(email)
            self.seen_email.add(email)
            return item
