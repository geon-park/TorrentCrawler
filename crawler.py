import requests
from lxml import html
import re


class TorrentCrawler:
    def __init__(self, base_url):
        self.BASE_URL = base_url

    def get_link(self, url, xpath, encoding='utf-8'):
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/61.0.3163.100 Safari/537.36'
        headers = {'User-Agent': user_agent}

        response = requests.get(url, headers=headers)
        if response.status_code != requests.codes.ok:
            return ''

        response.encoding = encoding
        root = html.fromstring(response.text)
        torrent_url = root.xpath(xpath)
        if torrent_url:
            return torrent_url[0]
        else:
            return ''

    def get_torrent_link(self, url, encoding='utf-8'):
        return self.BASE_URL + self.get_link(url, '//*[@id="file_table"]/tr[3]/td/a/@href', encoding)

    def get_magnet_link(self, url, encoding='utf-8'):
        return self.get_link(url, '//*[@id="main_body"]/table/tr/td/input/@value', encoding)

    def search_torrent(self, keyword, category='', encoding='utf-8'):
        url = self.BASE_URL + '/bbs/s.php'
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/61.0.3163.100 Safari/537.36'
        headers = {'User-Agent': user_agent}
        data = {'k': keyword, 'b': category}

        response = requests.get(url, headers=headers, params=data)
        if response.status_code != requests.codes.ok:
            return list()

        response.encoding = encoding
        root = html.fromstring(response.text)

        titles = [x.strip() for x in root.xpath('//*[@id="blist"]/table/tr/td[3]/a[2]/text()')]
        links = [self.BASE_URL + link[2:] for link in root.xpath('//*[@id="blist"]/table/tr/td[3]/a[2]/@href')]

        result_list = list(zip(titles, links))
        return result_list

    def get_top10(self, category, encoding='utf-8'):
        url = self.BASE_URL + '/' + category + '/torrent1.htm'
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/61.0.3163.100 Safari/537.36'
        headers = {'User-Agent': user_agent}

        response = requests.get(url, headers=headers)
        if response.status_code != requests.codes.ok:
            return list()

        response.encoding = encoding
        root = html.fromstring(response.text)

        titles = [x.strip() for x in root.xpath('//*[@id="bbs_latest_list"]/table/tr/td/a/text()')]
        links = [self.BASE_URL + link[2:] for link in root.xpath('//*[@id="bbs_latest_list"]/table/tr/td/a/@href')]

        result_list = list(zip(titles, links))
        return result_list
