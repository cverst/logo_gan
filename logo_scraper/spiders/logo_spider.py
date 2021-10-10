import scrapy
import csv
import urllib


def get_start_urls() -> list:
    """Return list of start_urls for LogoSpider

    Returns:
        list: ["url_1",
               "url_2",
               ...,
               "url_n]
    """

    # read company list from .csv
    companies = []
    with open("Forbes-2021.csv", "r", encoding="ISO-8859-1") as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # skip header
        for row in csvreader:
            companies.append(row[1])

    # create Wikipedia urls, some will not work, fix this later
    url_start = "https://en.wikipedia.org/wiki/"
    start_urls = [
        urllib.parse.urljoin(url_start, comp.replace(" ", "_")) for comp in companies
    ]

    return start_urls


class LogoItem(scrapy.Item):
    """LogoSpider output class

    Args:
        scrapy.Item: inherits from scrapy.Item class
    """

    company_name = scrapy.Field()
    wiki_name = scrapy.Field()
    wiki_url = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()


class LogoSpider(scrapy.Spider):
    """The spider retrieves logos of Wikipedia entries of companies in the Forbes
    2000 (2021) list. The Wikipedia URLs constructed from the Forbes 2000
    company names are not always leading to the corporation, and not all
    Wikipedia entries follow the scraping scheme used here. About 700 out of
    2000 companies therefore have no logo retrieved. Catching and correcting
    the errors is tedious so we accept the smaller, decently sized dataset.
    The list of images is manually checked for and pruned of erroneous images
    (e.g., buildings, all black images).

    Args:
        scrapy.Spider: inherits from scrapy.Spider class

    Yields:
        LogoItem class instances stored as logo_links.json and images stored
        in ./full. The LogoItem class instances contain references to the
        image locations.
    """

    name = "logo"

    def start_requests(self):
        return [scrapy.http.Request(url=start_url) for start_url in get_start_urls()]

    def parse(self, response):

        logo = LogoItem()

        logo["wiki_url"] = response._get_url()
        logo["company_name"] = logo["wiki_url"].split("/")[-1].replace("_", " ")

        info_items = response.css("table.infobox.vcard")
        logo["wiki_name"] = info_items.css("caption.infobox-title.fn.org::text").get()

        url_part = response.css("td.infobox-image.logo").css("img").attrib["src"]
        logo["image_urls"] = [urllib.parse.urljoin("https:", url_part)]

        yield logo
