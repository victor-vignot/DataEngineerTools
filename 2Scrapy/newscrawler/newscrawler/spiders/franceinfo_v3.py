import scrapy
from scrapy import Request


class FranceinfoSpider(scrapy.Spider):
    """Équivalent de lemonde_v3.py : on entre dans chaque rubrique et on
    récupère les articles listés (titre, image, description)."""
    name = "franceinfov3"
    allowed_domains = ["www.franceinfo.fr"]
    start_urls = ["https://www.franceinfo.fr/"]
    # Lien du bloc "rubriques" qui n'est pas une rubrique d'actualité
    excluded = ["/une-information-transparente-franceinfo/"]

    def parse(self, response):
        for link in response.css("#rubriques a.title-link__link"):
            if link.attrib["href"] in self.excluded:
                continue
            category = self.clean_spaces(" ".join(link.css("*::text").extract()))
            # cb_kwargs transmet le nom de la rubrique à la méthode de callback
            yield Request(
                response.urljoin(link.attrib["href"]),
                callback=self.parse_category,
                cb_kwargs={"category": category},
            )

    def parse_category(self, response, category):
        # Chaque article de la rubrique est une "carte" : <article class="card-article-base ...">
        for article in response.css("article.card-article-base"):
            title = self.clean_spaces(" ".join(article.css(".card-article-base__title::text").extract()))
            # Les images sont chargées en différé : la vraie adresse est dans data-src
            image = article.css("img::attr(data-src)").extract_first() or article.css("img::attr(src)").extract_first()
            description = self.clean_spaces(article.css(".card-article-base__chapo::text").extract_first())
            yield {
                "category": category,
                "title": title,
                "image": image,
                "description": description,
                "url": response.urljoin(article.css("a::attr(href)").extract_first()),
            }

    def clean_spaces(self, string):
        if string:
            return " ".join(string.split())
