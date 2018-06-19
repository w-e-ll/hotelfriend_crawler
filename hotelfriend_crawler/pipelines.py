# -*- coding: utf-8 -*-
from scrapy.exporters import JsonItemExporter
from hotelfriend_crawler.items import Description, Service, Deal


class JsonPipeline:
    def __init__(self):
        # exporter deal
        self.deal_file = open("deals.json", 'wb')
        self.deal_exporter = JsonItemExporter(self.deal_file, encoding='utf-8', ensure_ascii=True)
        self.deal_exporter.start_exporting()
        # exporter service
        self.service_file = open("services.json", 'wb')
        self.service_exporter = JsonItemExporter(self.service_file, encoding='utf-8', ensure_ascii=True)
        self.service_exporter.start_exporting()
        # exporter description
        self.description_file = open("hotels.json", 'wb')
        self.description_exporter = JsonItemExporter(self.description_file, encoding='utf-8', ensure_ascii=True)
        self.description_exporter.start_exporting()

    def close_spider(self, spider):
        # export deal
        self.deal_exporter.finish_exporting()
        self.deal_file.close()
        # export service
        self.service_exporter.finish_exporting()
        self.service_file.close()
        # export description
        self.description_exporter.finish_exporting()
        self.description_file.close()

    def process_item(self, item, spider):
        if isinstance(item, Deal):
            self.deal_exporter.export_item(item)
            return item
        if isinstance(item, Service):
            self.service_exporter.export_item(item)
            return item
        if isinstance(item, Description):
            self.description_exporter.export_item(item)
            return item

