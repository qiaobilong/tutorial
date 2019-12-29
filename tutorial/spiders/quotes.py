# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # 解析首页，并将数据传入Item
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuoteItem()
            item['text'] = quote.css('.text::text').get()
            item['author'] = quote.css('.author::text').get()
            item['tags'] = quote.css('.tags .tag::text').getall()
            yield item

        # 解析下一页url，并传递给request，同时调用parse递归
        next = response.css('.pager .next a::attr("href")').get()
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)
