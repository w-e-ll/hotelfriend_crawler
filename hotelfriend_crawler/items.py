# -*- coding: utf-8 -*-
from scrapy.item import Item, Field


class Description(Item):
    A_HOTEL_NAME = Field()
    DESCRIPTION_GRAY_TEXT_BG = Field()
    DESCRIPTION_TABLE = Field()
    DESCRIPTION_H2 = Field()
    DESCRIPTION_H3 = Field()
    DESCRIPTION_P = Field()
    DESCRIPTION_UL = Field()
    DESCRIPTION_BLOCKQUOTE = Field()


class Deal(Item):
    DEAL_SERVICE = Field()
    DEAL_NAME = Field()
    DEAL_PRICE = Field()


class Service(Item):
    SERVICE_CATEGORY = Field()
    SERVICE_CATEGORY_SUBCATEGORY = Field()
    SERVICE_CATEGORY_SUBCATEGORY_NAME = Field()
    SERVICE_CATEGORY_SUBCATEGORY_PRICE = Field()


