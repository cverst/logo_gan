import scrapy
import csv
import urllib
import os


def get_start_urls():
    # read company list from .csv
    companies = []
    with open("Forbes-2021.csv", "r", encoding="ISO-8859-1") as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # skip header
        for row in csvreader:
            companies.append(row[1])
    
    # create Wikipedia urls, some will not work, fix this later
    url_start = 'https://en.wikipedia.org/wiki/'
    start_urls = [urllib.parse.urljoin(url_start, comp.replace(' ', '_')) for comp in  companies]

    return start_urls


def image_full_filename(image_filename):
        full_filename = os.path.join(os.getcwd(), 'logo_images', image_filename)
        return full_filename


class LogoItem(scrapy.Item):
    company_name = scrapy.Field()
    wiki_name = scrapy.Field()
    wiki_url = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()


class LogoSpider(scrapy.Spider):
    name = 'logo'

    def start_requests(self):
        return [scrapy.http.Request(url=start_url) for start_url in get_start_urls()]

    def parse(self, response):
        
        logo = LogoItem()

        logo['wiki_url'] = response._get_url()
        logo['company_name'] = logo['wiki_url'].split('/')[-1].replace('_', ' ')
        
        info_items = response.css('table.infobox.vcard')
        logo['wiki_name'] = info_items.css('caption.infobox-title.fn.org::text').get()

        url_part = response.css('td.infobox-image.logo').css('img').attrib['src']
        logo['image_urls'] = [urllib.parse.urljoin('https:', url_part)]

        yield logo

