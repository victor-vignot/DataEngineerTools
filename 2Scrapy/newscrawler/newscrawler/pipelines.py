# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem


class TextPipeline(object):

    def process_item(self, item, spider):
        if item.get("title") and clean_spaces(item["title"]):
            item["title"] = clean_spaces(item["title"])
            if item.get("description"):
                item["description"] = clean_spaces(item["description"])
            return item
        else:
            raise DropItem(f"Missing title in {item}")


class MongoPipeline(object):
    """Stocke les items dans MongoDB (vu dans la partie 3Mongo).
    Non activé dans settings.py tant qu'aucun serveur Mongo ne tourne."""

    collection_name = "scrapy_items"

    def open_spider(self, spider):
        import pymongo
        self.client = pymongo.MongoClient()
        self.db = self.client["franceinfo"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item


def clean_spaces(string):
    if string:
        return " ".join(string.split())
