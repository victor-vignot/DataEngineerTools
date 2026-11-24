import scrapy
from scrapy import Request


class FranceinfoSpider(scrapy.Spider):
    """Équivalent de lemonde_v2.py pour franceinfo.fr.

    Le Monde bloque désormais Scrapy (erreur 406) et refuse ses pages de
    rubriques aux robots (erreur 402) : on applique la même démarche sur
    franceinfo, qui accepte les robots (voir https://www.franceinfo.fr/robots.txt).
    """
    name = "franceinfov2"
    allowed_domains = ["www.franceinfo.fr"]
    start_urls = ["https://www.franceinfo.fr/"]
    # Lien du bloc "rubriques" qui n'est pas une rubrique d'actualité
    excluded = ["/une-information-transparente-franceinfo/"]

    def parse(self, response):
        title = response.css("title::text").extract_first()
        # Les rubriques sont les titres de blocs de la section "Nos rubriques"
        # de la page d'accueil : <div id="rubriques"> ... <a class="title-link__link">
        all_links = {
            self.clean_spaces(" ".join(link.css("*::text").extract())): response.urljoin(link.attrib["href"])
            for link in response.css("#rubriques a.title-link__link")
            if link.attrib["href"] not in self.excluded
        }
        yield {
            "title": title,
            "all_links": all_links,
        }

    def clean_spaces(self, string):
        if string:
            return " ".join(string.split())
