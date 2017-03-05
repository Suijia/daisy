#!/usr/bin/env python
# -*-coding:utf-8-*-
import requests
import time
from lxml import etree
from utils.CrawlerLogger import CrawlerLogger
import crawler.util as util
from model import Doc

__author__ = 'yangxj'

# ==============================
# author: yangxj
# created at: 16/8/7 上午9:19
# filename: SWFAdapter.py
# ==============================


class SWFAdapter:
    def __init__(self, seed_url='http://www.sfw.com.cn/?cat=9', source=u'科幻世界', channel=u"资讯"):
        self.seed_url = seed_url
        self.source = source
        self.channel = channel

    def get_docs(self):
        doc_list = list()
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) "
                                     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
            r = requests.get(self.seed_url, headers=headers)
            if r.status_code == 200:
                html_text = r.text
            else:
                CrawlerLogger.logger.info("request seed_url error {0} status: {1}".format(self.seed_url, r.status_code))
                return doc_list
        except Exception as e:
            CrawlerLogger.logger.info("request seed_url error {0} {1}".format(self.seed_url, e))
            return doc_list

        html = etree.HTML(html_text)
        channel = util.get_text(html, '//div[@class="block archive"]/h3', True).strip()
        if channel and channel != "":
            CrawlerLogger.logger.info("get channel {0}".format(channel.encode('utf-8')))
            self.channel = channel
        result = html.xpath('//div[@class="block archive"]/div')
        # print type(result)
        # print len(result)
        CrawlerLogger.logger.info("result size: {0}".format(len(result)))
        index = 0
        for item in result[0: -1]:
            CrawlerLogger.logger.info('--------------------' + str(index))
            index += 1
            # print type(item)
            # print etree.tostring(item)

            title = util.get_text(item, './/h2/a/@title', False)
            detail_url = util.get_text(item, './/h2/a/@href', False)
            snippet = util.get_text(item, './/p', True)
            cover = util.get_text(item, './/div[@class="block-image"]/a/img/@src', False)
            author = util.get_text(item, './/span[@class="heading-author"]', True)
            published_str_raw = util.get_text(item, './/span[@class="heading-date"]', True)

            published_str = published_str_raw
            published_str = published_str.replace(u'十一月', '11')
            published_str = published_str.replace(u'十二月', '12')
            published_str = published_str.replace(u'一月', '01')
            published_str = published_str.replace(u'二月', '02')
            published_str = published_str.replace(u'三月', '03')
            published_str = published_str.replace(u'四月', '04')
            published_str = published_str.replace(u'五月', '05')
            published_str = published_str.replace(u'六月', '06')
            published_str = published_str.replace(u'七月', '07')
            published_str = published_str.replace(u'八月', '08')
            published_str = published_str.replace(u'九月', '09')
            published_str = published_str.replace(u'十月', '10')

            try:
                published_time = int(time.mktime(time.strptime(published_str, "%m %d, %Y")))
            except Exception as e:
                published_time = time.time()
                CrawlerLogger.logger.info("get publish time error {0}, {1}".format(
                    published_str_raw.encode('utf-8'), published_str))
                print e

            doc = Doc(self.source, title, detail_url, snippet, cover, author, self.channel, published_time)
            CrawlerLogger.logger.info("get doc" + str(doc))
            doc_list.append(doc)
        return doc_list


if __name__ == '__main__':
    adapter = SWFAdapter(seed_url='http://www.sfw.com.cn/?cat=9')
    adapter.get_docs()

    timeArray = time.strptime("2013-10-10 23:40:00","%Y-%m-%d %H:%M:%S")
    timeStamp =int(time.mktime(timeArray))
