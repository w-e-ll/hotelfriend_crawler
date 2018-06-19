# -*- coding: utf-8 -*-
import json
import logging
import urllib.request

from pprint import pprint
from scrapy.utils.log import configure_logging
from scrapy import Spider
from scrapy.http import Request
from hotelfriend_crawler.items import Description, Service, Deal

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger()


class HotelSpider(Spider):

    name = 'hotel'
    allowed_domains = ['hotelfriend.com']
    start_urls = ['https://hotelfriend.com/s']

    def parse(self, response):
        """ Parse and extract hotel urls and next page url """

        # process hotels
        hotels = response.xpath('//hf-hotel-search-result-item/a/@href').extract()
        for hotel in hotels:
            absolute_url = response.urljoin(hotel)
            yield Request(absolute_url, callback=self.parse_hotels)

        # process next page
        next_page_url = response.xpath('//div[@class="hf-flexbox middle center page next"]/a/@href').extract_first()
        if next_page_url is not None:
            absolute_next_page_url = response.urljoin(next_page_url)
            yield Request(absolute_next_page_url)

    def parse_hotels(self, response):
        """ Process name & description + deals urls / services"""
        description = Description()
        service = Service()

        # process hotel description name:
        hotel_name = response.xpath('//h2[@class="title type-1 ng-star-inserted"]/text()').extract()
        description['A_HOTEL_NAME'] = hotel_name

        # process description grey_text_bg:
        description_grey_text_bg = response.xpath('//div[@class="grey-text-bg"]/p/text()').extract_first()
        description['DESCRIPTION_GRAY_TEXT_BG'] = description_grey_text_bg

        # process description table:
        description_table = response.xpath(
            '//div[@class="p1 ng-star-inserted"]/table/tbody/tr/td/following-sibling::td/text()').extract()
        description['DESCRIPTION_TABLE'] = description_table

        # process description h2:
        description_h2 = response.xpath('//div[@class="p1 ng-star-inserted"]/h2/text()').extract()
        description['DESCRIPTION_H2'] = description_h2

        # process description h3:
        description_h3 = response.xpath('//div[@class="p1 ng-star-inserted"]/h3/text()').extract()
        description['DESCRIPTION_H3'] = description_h3

        # process description p:
        description_p = response.xpath('//div[@class="p1 ng-star-inserted"]/p/text()').extract()
        description['DESCRIPTION_P'] = description_p

        # process description ul:
        description_ul = response.xpath(
            '//div[@class="p1 ng-star-inserted"]/ul/li/following-sibling::li/text()').extract()
        description['DESCRIPTION_UL'] = description_ul

        # process description blockquote:
        description_blockquote = response.xpath('//div[@class="p1 ng-star-inserted"]/blockquote/text()').extract()
        description['DESCRIPTION_BLOCKQUOTE'] = description_blockquote

        # process hotel deals urls:
        hotel_deal_urls = response.xpath('//hf-deal-item/a/@href').extract()
        for deal_url in hotel_deal_urls:
            url = response.urljoin(deal_url)
            yield Request(url, callback=self.parse_deals)

        # extract hotel_service_category_names:
        service_category = response.xpath('//h4[@class="catName"]/text()').extract()
        service['SERVICE_CATEGORY'] = service_category
        hotel_link_name = response.url.split('/a/')[1]

        # making hotel_api_urls to extract category data
        hotel_api_urls = []
        for a_category in service_category:
            hotel_api_url = 'https://api.hotelfriend.com/v2/search/' + hotel_link_name + \
                            '/services?substring={}'.format(a_category.replace(" ", "%20"))
            hotel_api_urls.append(hotel_api_url)

        # collecting hotel_category_id from hotel_api_urls
        hotel_services_category_ids = []
        for a_hotel_api_url in hotel_api_urls:
            a_hotel_api_url_data = urllib.request.urlopen(
                a_hotel_api_url.replace("\xe9", "\\xe9").replace("\xe4", "\\xe4").replace(
                    "\xf6", "\\xf6").replace("\xfc", "\\xfc").replace("\xe8", "\\xe8"))
            data = a_hotel_api_url_data.read()

            try:
                json_data = json.loads(data.decode("utf8", "escape"))
                hotel_services_category_id = json_data['categories'][0]['id']
                hotel_services_category_ids.append(hotel_services_category_id)

            except IndexError as err:
                category_id_error = '==> NO ID ADDED, look for error in API, no service category found!!! ' + \
                                    a_hotel_api_url, err
                pprint('================')
                pprint(category_id_error)
                pprint('================')
                self.logger.info(category_id_error)
                continue

        # making hotel_services_category_urls
        for hotel_services_category_id in hotel_services_category_ids:
            hotel_services_category_url = 'https://hotelfriend.com/a/' + hotel_link_name + \
                                          '/(alpha:subcategories/' + hotel_services_category_id + ')#services'
            yield Request(url=hotel_services_category_url,
                          callback=self.parse_services_category_subcategories)
        try:
            yield service
            yield description

        except Exception as error:
            logger.info(error)

    def parse_deals(self, response):
        """ Process hotel deals: """
        deal = Deal()

        # process deal service:
        deal_service = response.xpath('//div[@class="serviceName"]/text()').extract()
        deal['DEAL_SERVICE'] = deal_service

        # process deal name:
        deal_name = response.xpath('//h2[@class="dHead full-screen-title ng-star-inserted"]/text()').extract()
        deal['DEAL_NAME'] = deal_name

        # process deal price:
        deal_price = response.xpath('//span[@class="price small-euro"]/text()').extract_first().replace("\xa0", " ")
        deal['DEAL_PRICE'] = deal_price

        try:
            yield deal

        except Exception as error:
            logger.info(error)

    def parse_services_category_subcategories(self, response):
        """ Process hotel services category subcategories: """
        service = Service()

        # extract service_category_subcategory:
        service_category_subcategory = response.xpath('//h4[@class="catName"]/text()').extract()
        service['SERVICE_CATEGORY_SUBCATEGORY'] = service_category_subcategory
        # process hotel link:
        hotel_link_name = response.xpath(
            '//a[@class="hf-header-menu-lang_link"]/@href').extract_first().split('/(')[0].replace("/de/a/", "")

        # making hotel_api_urls to extract category data
        hotel_api_urls = []
        for subcategory in service_category_subcategory:
            hotel_api_url = 'https://api.hotelfriend.com/v2/search/' + hotel_link_name + \
                      '/services?substring={}'.format(subcategory.replace(" ", "%20"))
            hotel_api_urls.append(hotel_api_url)

        # collecting hotel_category_subcategory_id from hotel_api_urls
        hotel_services_category_subcategory_ids = []
        for a_hotel_api_url in hotel_api_urls:
            a_hotel_api_url_data = urllib.request.urlopen(
                a_hotel_api_url.replace("\xe9", "\\xe9").replace("\xe4", "\\xe4").replace(
                    "\xf6", "\\xf6").replace("\xfc", "\\xfc").replace("\xe8", "\\xe8"))
            data = a_hotel_api_url_data.read()

            try:
                json_data = json.loads(data.decode("utf8", "escape"))
                hotel_services_category_subcategory_id = json_data['subcategories'][0]['id']
                hotel_services_category_subcategory_ids.append(hotel_services_category_subcategory_id)

            except IndexError as err:
                subcategory_id_error = '==> NO SUBCATEGORY ID ADDED, look for error in API, no subcategory found!!! ' + \
                                       a_hotel_api_url, err
                pprint('===================')
                pprint(subcategory_id_error)
                pprint('===================')
                self.logger.info(subcategory_id_error)
                continue

        # making hotel_service_category_urls
        full_hotel_link_name = response.xpath(
            '//a[@class="hf-header-menu-lang_link"]/@href').extract_first().replace("/de/a/", "").replace(")", "")
        for subcategory_id in hotel_services_category_subcategory_ids:
            category_subcategory_url = 'https://hotelfriend.com/a/' + full_hotel_link_name + \
                                       '/services/' + subcategory_id + ')#services'
            yield Request(url=category_subcategory_url,
                          callback=self.parse_services_category_subcategory_names_and_prices)
        try:
            yield service

        except Exception as error:
            logger.info(error)

    def parse_services_category_subcategory_names_and_prices(self, response):
        """ Process hotel services category subcategory names and prices: """
        service = Service()

        # extract service_category_subcategory name:
        service_category_subcategory_name = response.xpath('//h4[@class="card-title"]/text()').extract()
        service['SERVICE_CATEGORY_SUBCATEGORY_NAME'] = service_category_subcategory_name

        # extract service_category_subcategory price:
        service_category_subcategory_price = response.xpath('//div[@class="price small-euro"]/text()').extract()
        service_category_subcategory_price = str(service_category_subcategory_price).replace("\\xa0", " ").strip("'['").strip("']'")
        service['SERVICE_CATEGORY_SUBCATEGORY_PRICE'] = service_category_subcategory_price

        try:
            yield service

        except Exception as error:
            logger.info(error)
