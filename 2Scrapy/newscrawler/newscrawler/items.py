# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    image = scrapy.Field()
    description = scrapy.Field()
    # Champs ajoutés pour la version franceinfo
    category = scrapy.Field()
    url = scrapy.Field()
