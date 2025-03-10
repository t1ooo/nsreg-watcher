# -*- coding: utf-8 -*-
import scrapy
from nsreg.items import NsregItem

from ..utils import find_price
# работает

REGEX_PATTERN = r"([0-9]+)\s+₽.*"
EMPTY_PRICE = {
    'price_reg': None,
    'price_prolong': None,
    'price_change': None,
}


class NsregDnsSpider(scrapy.Spider):
    name = "nsreg_dns"
    allowed_domains = ["fastdns.ru"]
    start_urls = ["https://fastdns.ru/#price"]

    def parse(self, response):
        price_reg = response.xpath(
            '/html/body/div[1]/div[4]/div/div[2]/div[3]/div/div/div/div[2]/div/div/div[1]/div/table/tbody/tr[2]/td[2]/div/p/text()').get()
        price_reg = find_price(REGEX_PATTERN, price_reg)

        price_prolong = response.xpath(
            '/html/body/div[1]/div[4]/div/div[2]/div[3]/div/div/div/div[2]/div/div/div[1]/div/table/tbody/tr[3]/td[2]/div/p/text()').get()
        price_prolong = find_price(REGEX_PATTERN, price_prolong)

        price_change = response.xpath(
            '/html/body/div[1]/div[4]/div/div[2]/div[3]/div/div/div/div[2]/div/div/div[1]/div/table/tbody/tr[4]/td[2]/div/p/text()').get()
        price_change = find_price(REGEX_PATTERN, price_change)

        item = NsregItem()
        item['name'] = "ООО «ДНС»"
        price = item.get('price', EMPTY_PRICE)
        price['price_reg'] = price_reg
        price['price_prolong'] = price_prolong
        price['price_change'] = price_change
        item['price'] = price

        yield item
