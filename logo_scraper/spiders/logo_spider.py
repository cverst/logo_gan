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
    """A spider that retrieves company logos from Wikipedia.
    
    Wikipedia URLs are reconstructed for companies in the Forbes 2000 (year
    2021) list. These URLs do not always lead to the company's WIkipedia entry
    and not all Wikipedia entries follow the same HTML scheme. Errors will be
    raised for these companies.

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
