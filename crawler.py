import urllib.request
from lxml import html
import re


class TorrentCrawler:
    BASE_URL = "https://torrentkim10.net/"

    def __init__(self):
        pass

    def make_url(self, keyword, category=''):
        url = self.BASE_URL + 'bbs/s.php?k=' + urllib.request.quote(keyword) + '&b=' + category
        return url

    def search_torrent(self, keyword, category='', decode='utf-8'):
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/61.0.3163.100 Safari/537.36'

        req = urllib.request.Request(self.make_url(keyword, category), headers={'User-Agent': user_agent})
        content = urllib.request.urlopen(req).read()
        root = html.fromstring(content)

        # must remove tbody(//*[@id="blist"]/table/tr[3]/td[3]/a[2] -> tr[x] is loop)
        ''' for tags in root.xpath('//*[@id="blist"]/table/tr/td[3]/a[2]'):
            title = tags.xpath('.//text()')[0].strip()
            link = tags.xpath('.//@href')[0].strip()
            print(title + '-----' + link)
        '''
        magnets_list = root.xpath('//*[@id="blist"]/table/tr/td[1]/a/@href')
        titles_list = root.xpath('//*[@id="blist"]/table/tr/td[3]/a[2]/text()')
        links_list = root.xpath('//*[@id="blist"]/table/tr/td[3]/a[2]/@href')
        # remove first element of magnets(ad)
        magnets_list = magnets_list[1:]

        p = re.compile('[A-F0-9]{40}') # extract magnet hash key
        magnets = [p.search(x).group() for x in magnets_list]
        titles = [x.strip() for x in titles_list]
        links = [x for x in links_list]

        result_list = list(zip(magnets, titles, links))
        return result_list
