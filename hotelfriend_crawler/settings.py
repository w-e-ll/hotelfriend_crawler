# -*- coding: utf-8 -*-

BOT_NAME = 'hotelfriend_crawler'

SPIDER_MODULES = ['hotelfriend_crawler.spiders']
NEWSPIDER_MODULE = 'hotelfriend_crawler.spiders'

USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
HTTPCACHE_ENABLED = True

ITEM_PIPELINES = {
    'hotelfriend_crawler.pipelines.JsonPipeline': 300,
}
