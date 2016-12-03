import scrapy
from scrapy.selector import Selector
import os
import os.path


class MySpider(scrapy.Spider):
    name = "base_spider"
    base_dir = "www_roots"
    cur_root_dirname = ""
    cur_root_url = ""

    def start_requests(self):
        urls = [
            'http://www.concordia.ca/artsci/biology.html',
            'http://www.concordia.ca/artsci/chemistry.html',
            'http://www.concordia.ca/artsci/exercise-science.html',
            'http://www.concordia.ca/artsci/geography-planning-environment.html',
            'http://www.concordia.ca/artsci/math-stats.html',
            'http://www.concordia.ca/artsci/physics.html',
            'http://www.concordia.ca/artsci/psychology.html',
            'http://www.concordia.ca/artsci/science-college.html'
        ]

        # create dir for the root page
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        for url in urls:
            # www.example.com/foo/bar
            self.cur_root_url = url.split('://')[1]
            self.cur_root_url = url.split('.html')[0]
            print (self.cur_root_url)

            # www_root/bar
            self.cur_root_dirname = self.base_dir + "/" + self.cur_root_url.split('/')[-1]

            # create dir for the current sub-root page
            if not os.path.exists(self.cur_root_dirname):
                os.makedirs(self.cur_root_dirname)

            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # example.html
        page = response.url.split("/")[-1]
        if '.' in page:
            page_type = str(page).split('.')[1]
        else:
            page_type = ""
        # example
        filename = str(page).split('.')[0]

        if page_type == "html":

            # handle file saving and append count if filename exists
            count = 1
            if not os.path.isfile(self.cur_root_dirname + '/' + page):
                with open(self.cur_root_dirname + '/' + filename + ".txt", 'a') as f:
                    site = get_tags(response)
                    f.write(site.encode('utf-8', 'ignore'))
                self.log('Saved file %s' % filename)
            else:
                while os.path.isfile(self.cur_root_dirname + '/' + filename + str(count) + ".txt"):
                    count += 1
                with open(self.cur_root_dirname + '/' + filename + str(count) + ".txt", 'a') as f:
                    site = get_tags(response)
                    f.write(site.encode('utf-8', 'ignore'))
                self.log('Saved file %s' % page)

            # follow url
            for href in response.css('a::attr(href)').extract():
                # if starts with slash and not moving up dirs
                utf = str(href).encode('utf-8', 'ignore')
                if utf.startswith('/') and ".." not in utf:
                    # COULD CHECK IF FILE EXISTS BEFORE EVEN SENDING REQUEST?, SAVE BANDWIDTH
                    yield scrapy.Request(response.urljoin(href),
                                         callback=self.parse)


def get_tags(response):
    site = ''.join(response.xpath("//p//text()").extract()).strip()
    site += ''.join(response.xpath("//h1//text()").extract()).strip()
    site += ''.join(response.xpath("//h2//text()").extract()).strip()
    site += ''.join(response.xpath("//h3//text()").extract()).strip()
    site += ''.join(response.xpath("//h4//text()").extract()).strip()
    site += ''.join(response.xpath("//h5//text()").extract()).strip()
    site += ''.join(response.xpath("//h6//text()").extract()).strip()
    return site