import scrapy


class ChurchillQuotesSpider(scrapy.Spider):
    name = "citations de Churchill"
    start_urls = ["https://evene.lefigaro.fr/citations/winston-churchill", ]
    # Pour que les accents restent lisibles dans le fichier JSON exporté
    custom_settings = {"FEED_EXPORT_ENCODING": "utf-8", "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7"}

    def parse(self, response):
        # Le site a été refait depuis l'écriture du cours : chaque citation est
        # maintenant dans <article class="fig-quote">, le texte dans
        # <p class="fig-quote__text"><a>...</a></p> et l'auteur dans
        # <a class="fig-link fig-credit__author">.
        for cit in response.xpath('//article[@class="fig-quote"]'):
            text_value = cit.xpath('.//p[@class="fig-quote__text"]/a/text()').extract_first()
            author = cit.xpath('.//a[contains(@class, "fig-credit__author")]/text()').extract_first()

            text_value = self.clean_quote(text_value)
            author = author.strip() if author else None

            # On ne garde que les citations de Winston Churchill
            if text_value and author == "Winston Churchill":
                yield {"text": text_value, "author": author}

    def clean_quote(self, text):
        """Retire les guillemets “ (U+201C) et ” (U+201D) et les espaces superflus."""
        if text is None:
            return None
        text = text.replace("\u201c", "").replace("\u201d", "")
        return " ".join(text.split())
