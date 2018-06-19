# HotelFriend-Crawler

HotelFriend-Crawler is a python web spyder developed with Scrapy framework.
Spider scrapes hotel descriptions, deals, services from https://hotelfriend.com/. 
Scraped data stored in json files.

### Dependencies

- Python3
- Scrapy

### Task

Parse all hotels from https://hotelfriend.com/s
For each hotel scrape:
- Text description.
- Services for this hotel. For each service download price, name,
name of category.
- Deals. For each deal download price, name, services, that included
into this deal.
Save the scraped data in form of three CSV or JSON files (files for hotels,
services and deals accordingly).

### Make Initial Setup

1. virtualenv -p python3 hotelfriend_crawler
2. cd hotelfriend_crawler
3. activate it (source bin/activate)
4. git clone https://github.com/w-e-ll/hotelfriend_crawler.git
5. cd hotelfriend_crawler
6. pip install -r requirements.txt
7. cd hotelfriend_crawler
8. python run.py

made by: https://w-e-ll.com
