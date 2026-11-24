import scrapy
from scrapy import Request

from ..items import ArticleItem


class FranceinfoSpider(scrapy.Spider):
    """Équivalent de lemonde_v4.py : les articles sont renvoyés sous forme
    d'ArticleItem (voir items.py) et passent par les pipelines (voir settings.py)."""
    name = "franceinfov4"
    allowed_domains = ["www.franceinfo.fr"]
    start_urls = ["https://www.franceinfo.fr/"]
    # Lien du bloc "rubriques" qui n'est pas une rubrique d'actualité
    excluded = ["/une-information-transparente-franceinfo/"]

    def parse(self, response, **kwargs):
        for link in response.css("#rubriques a.title-link__link"):
            if link.attrib["href"] in self.excluded:
                continue
            category = " ".join(" ".join(link.css("*::text").extract()).split())
            yield Request(
                response.urljoin(link.attrib["href"]),
                callback=self.parse_category,
                cb_kwargs={"category": category},
            )

    def parse_category(self, response, category):
        for article in response.css("article.card-article-base"):
            # Plus besoin de clean_spaces ici : c'est le TextPipeline qui nettoie le titre
            yield ArticleItem(
                category=category,
                title=" ".join(article.css(".card-article-base__title::text").extract()),
                image=article.css("img::attr(data-src)").extract_first() or article.css("img::attr(src)").extract_first(),
                description=article.css(".card-article-base__chapo::text").extract_first(),
                url=response.urljoin(article.css("a::attr(href)").extract_first()),
            )
