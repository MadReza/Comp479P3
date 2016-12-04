import scrapy
from scrapy.selector import Selector
import os
import os.path
import sys

class MySpider(scrapy.Spider):
    name = "base_spider"
    base_dir = "../www_roots"
    cur_root_url = ""

    folder_size_dict = {}
    Max_Folder_Size = 1048576*2 #1MB*2 = 2MB

    def start_requests(self):
        urls = [
            'http://www.concordia.ca/artsci/biology.html',
            'http://www.concordia.ca/artsci/chemistry.html',
            'http://www.concordia.ca/artsci/exercise-science.html',
            'http://www.concordia.ca/artsci/geography-planning-environment.html',
            'http://www.concordia.ca/artsci/math-stats.html',
            'http://www.concordia.ca/artsci/physics.html',
            'http://www.concordia.ca/artsci/psychology.html',
            'http://www.concordia.ca/artsci/science-college.html',
            'https://www.concordia.ca/artsci/science-college/about/life-at-the-college.html'
        ]
        #last link is the secret page

        # create dir for the root page
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        for url in urls:
            # www.example.com/foo/bar
            self.cur_root_url = url.split('://')[1]
            self.cur_root_url = url.split('.html')[0]
            print (self.cur_root_url)

            # e.g. Biology (used to keep record in size dictionary)
            department = self.cur_root_url.split('/')[-1]
            # www_root/bar
            cur_root_dirname = self.base_dir + "/" + department

            # init departments folder size
            print ("DICT STAT")
            self.folder_size_dict[department] = sum(os.path.getsize(cur_root_dirname + '/' + f) for f in os.listdir(cur_root_dirname) if os.path.isfile(cur_root_dirname + '/' + f))
            print (self.folder_size_dict)

            # create dir for the current sub-root page
            if not os.path.exists(cur_root_dirname):
                os.makedirs(cur_root_dirname)

            if self.folder_size_dict[department] < self.Max_Folder_Size:
                request = scrapy.Request(url=url, callback=self.parse)
                request.meta['cur_root_dirname'] = cur_root_dirname
                request.meta['department'] = department
                yield request

    def parse(self, response):
        cur_root_dirname = response.meta['cur_root_dirname']
        department = response.meta['department']

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
            if not os.path.isfile(cur_root_dirname + '/' + page):

                write_to_file(self, response, cur_root_dirname, department, filename)
            else:
                while os.path.isfile(cur_root_dirname + '/' + filename + str(count) + ".txt"):
                    count += 1
                write_to_file(self, response, cur_root_dirname, department, filename)

            # follow url if current dept folder size is under (1MB) ?
            if self.folder_size_dict[department] < self.Max_Folder_Size:
                for href in response.css('a::attr(href)').extract():
                    # if starts with slash and not moving up dirs
                    utf = str(href).encode('utf-8', 'ignore')
                    if utf.startswith('/') and ".." not in utf:
                        request = scrapy.Request(response.urljoin(href), callback=self.parse)
                        request.meta['cur_root_dirname'] = cur_root_dirname
                        request.meta['department'] = department
                        yield request


def write_to_file(self, response, cur_root_dirname, department, filename):
    with open(cur_root_dirname + '/' + filename + ".txt", 'a') as f:
        site = get_tags(response)
        f.write(site.encode('utf-8', 'ignore'))
    self.log('Saved file %s' % filename)
    self.folder_size_dict[department] += sys.getsizeof(site)


def get_tags(response):
    site = ''.join(response.xpath("//p//text()").extract()).strip()
    site += ''.join(response.xpath("//h1//text()").extract()).strip()
    site += ''.join(response.xpath("//h2//text()").extract()).strip()
    site += ''.join(response.xpath("//h3//text()").extract()).strip()
    site += ''.join(response.xpath("//h4//text()").extract()).strip()
    site += ''.join(response.xpath("//h5//text()").extract()).strip()
    site += ''.join(response.xpath("//h6//text()").extract()).strip()
    return site
