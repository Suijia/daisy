#!/usr/bin/env python
# -*-coding:utf-8-*-
import json
from lxml import etree
import requests
from utils.CrawlerLogger import CrawlerLogger
import crawler.util as util
from model import Doc
import re

__author__ = 'yangxj'

# ==============================
# author: yangxj
# created at: 16/8/7 上午9:19
# filename: SWFAdapter.py
# ==============================
# 微信公众号
#
# - 不存在日报
# - 幻象文库
# - 科幻世界
# - 星云网
# - 机器之心
# - 大都会新闻


class MediaPressAdapter:

    FIX_PARM = "&devicetype=Windows-QQBrowser&version=61030004&pass_ticket=qMx7ntinAtmqhVn+C23mCuwc9ZRyUp20kIusGgbFLi0=&uin=MTc1MDA1NjU1&ascene=1"

    def __init__(self, seed_url='', source=u'微信公众号', channel=u"不存在"):
        self.seed_url = seed_url
        self.source = source
        self.channel = channel
        self.headers = {'Referer': 'http://mp.weixin.qq.com/profile',
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) "
                                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}

    def get_docs(self):
        doc_list = list()

        query_html_text = self.get_query_content(self.seed_url)
        if query_html_text == "":
            CrawlerLogger.logger.error("get query html content error {0}".format(self.seed_url.encode('utf-8')))
            return doc_list

        latest_doc = self.get_latest_doc(query_html_text)
        if latest_doc:
            CrawlerLogger.logger.info("get latest doc succ")
            doc_list.append(latest_doc)
        list_url = MediaPressAdapter.get_list_url(query_html_text)

        html_text = self.get_list_content(list_url)
        if html_text == "":
            CrawlerLogger.logger.info("ger list page content error" + list_url)
            return doc_list

        list_strs = re.findall(r"var msgList = (.*)]};", html_text)
        if len(list_strs) == 0:
            CrawlerLogger.logger.info("ger list str error" + html_text)
            return doc_list
        list_str = list_strs[0] + "]}"
        list_str = list_str.replace('&quot;', '"').replace('&amp;', '&')
        list_str = list_str.replace('&lt;', '<').replace('&gt;', '<')
        list_str = list_str.replace('\\\\', '').replace('}&quot;', '')
        list_str = list_str.replace('&amp;', '&')

        if isinstance(list_str, unicode):
            CrawlerLogger.logger.info("get list url {0}".format(list_str.encode('utf-8')))
        else:
            CrawlerLogger.logger.info("get list url {0}".format(list_str))

        results = json.loads(list_str)
        CrawlerLogger.logger.info("result size: {0}".format(len(results.get('list', list()))))
        index = 0
        for item_info in results.get('list', list())[0:3]:
            CrawlerLogger.logger.info('--------------------' + str(index))
            index += 1
            item = item_info.get('app_msg_ext_info', dict())
            published_time1 = item_info.get('comm_msg_info', dict()).get('datetime', 0)
            try:
                published_time = int(published_time1)
            except Exception as e:
                CrawlerLogger.logger.warn("get error published time {0}".format(published_time1) + str(e))
                continue
            doc = self.get_doc_from_info(item, published_time)
            if doc is None:
                continue
            doc_list.append(doc)
            if item.get('is_multi', 0) == 0:
                continue
            ext_index = 0
            for item_ext in item.get('multi_app_msg_item_list', list()):
                CrawlerLogger.logger.info('--------------------' + str(index) + " EXT " + str(ext_index))
                ext_index += 1
                doc_ext = self.get_doc_from_info(item_ext, published_time)
                if doc_ext is None:
                    continue
                doc_list.append(doc_ext)

        return doc_list

    def get_doc_from_info(self, item, published_time):
        title = item.get('title', "")
        detail_url_tmp = "http://mp.weixin.qq.com" + item.get('content_url', "")
        detail_content = self.get_detail_content(detail_url_tmp)
        if detail_content == "":
            return None
        detail_url = self.get_detail_url(detail_content)
        if detail_url == "":
            CrawlerLogger.logger.warn("get detail url error {0}".format(detail_url_tmp))
            return None
        snippet = item.get('digest', "")
        cover = item.get('cover', "")
        author = item.get('author', "")

        doc = Doc(self.source, title, detail_url, snippet, cover, author, self.channel, published_time)
        CrawlerLogger.logger.info("get doc" + str(doc))
        return doc

    def get_list_content(self, list_url = ""):
        util.print_sleep(30, 1, "ready to get media press doc list page")
        CrawlerLogger.logger.info("list_url: " + list_url)
        # list 页经常要求输入验证码, 多刷新几下可能成功
        try_time = 0
        while try_time < 10:
            try:
                r = requests.get(list_url, headers=self.headers)
                if r.status_code == 200:
                    html_text = r.text
                    if u"为了保护你的网络安全，请输入验证码" in html_text:
                        CrawlerLogger.logger.error("request list content error, need confirm code")
                    else:
                        return r.text
                else:
                    CrawlerLogger.logger.info("request list_url error {0} status: {1}".format(list_url, r.status_code))
            except Exception as e:
                CrawlerLogger.logger.info("request list_url error {0}".format(list_url) + e.message)
            util.print_sleep(10, 1, "some thing error try again " + str(try_time))
            try_time += 1

        return ""

        # print html_text

        # fp = open('bin/crawler/adapter/list.html', 'r')
        # html_text = fp.read()
        # return html_text

    def get_detail_content(self, tmp_url_in, pause=True):
        """
        获取详情页内容
        :param pause: 抓取前是否延迟
        :param tmp_url: 带时间戳的临时url
        :return:
        """
        if pause:
            util.sleep_random(50, 100, 10, "ready to get media press detail url")  # 随机休息
        tmp_url = tmp_url_in + MediaPressAdapter.FIX_PARM
        CrawlerLogger.logger.info("temp url: " + tmp_url)
        try:
            r = requests.get(tmp_url, headers=self.headers)
            if r.status_code == 200:
                return r.text
            else:
                CrawlerLogger.logger.warn("request tmp_url error {0} status: {1}".format(self.seed_url, r.status_code))
                return ""
        except Exception as e:
            CrawlerLogger.logger.warn("request tmp_url error {0} {1}".format(self.seed_url, e))
            return ""

        # fp = open('bin/crawler/adapter/mp_detail.html', 'r')
        # html_text = fp.read()
        #
        # return html_text.decode("utf-8")

    @staticmethod
    def get_detail_url(detail_content):
        list_strs = re.findall(r'var msg_link = "(.*)"', detail_content)
        if len(list_strs) == 0:
            CrawlerLogger.logger.warn("ger list str error" + detail_content)
            return ""
        for xxx in list_strs:
            CrawlerLogger.logger.info("xxx detail url: " + xxx)
        list_str = list_strs[0]
        CrawlerLogger.logger.info("detail url: " + list_str)
        list_str = list_str.replace('&amp;', '&')
        CrawlerLogger.logger.info("detail url: " + list_str)
        list_str = list_str.replace('\x26amp;', '&')
        CrawlerLogger.logger.info("detail url: " + list_str)
        list_str = list_str.replace('\\x26amp;', '&')
        CrawlerLogger.logger.info("detail url: " + list_str)
        return list_str

    def get_query_content(self, query_url):
        """
        获取query页的页面内容
        :param query_url:
        :return:
        """
        CrawlerLogger.logger.info("query url: " + query_url)
        try:
            r = requests.get(query_url, headers=self.headers)
            if r.status_code == 200:
                return r.text
            else:
                CrawlerLogger.logger.info(
                    "request query_url error {0} status: {1}".format(self.seed_url, r.status_code))
                return ""
        except Exception as e:
            CrawlerLogger.logger.info("request query_url error {0} {1}".format(self.seed_url, e))
            return ""

        # util.print_sleep(30, 1, "ready to get media press list url")

        # fp = open('bin/crawler/adapter/mp_query.txt', 'r')
        # html_text = fp.read()
        # return html_text

    @staticmethod
    def get_list_url(query_html_text):
        # list_strs = re.findall(r'onclick="gotourl\(\'(.*?)\'', query_html_text)
        html = etree.HTML(query_html_text)
        tmp_list_url = util.get_text(html, '//div[@class="txt-box"]/p/a/@href', False)
        CrawlerLogger.logger.info("tmp_detail_url: " + tmp_list_url)

        list_str = tmp_list_url
        list_str = list_str.replace('&amp;', '&')
        list_str = list_str.replace('\x26amp;', '&')
        CrawlerLogger.logger.info("list url: " + list_str)
        return list_str

    def get_latest_doc(self, query_html_text):
        """
        直接从query页看到新最新的一篇文章
        :param query_html_text:
        :return:
        """
        html = etree.HTML(query_html_text)
        # print query_html_text
        tmp_detail_url = util.get_text(html, '//div[@class="news-box"]/ul/li/dl/dd/a/@href', False)
        CrawlerLogger.logger.info("tmp_detail_url: " + tmp_detail_url)

        detail_content = self.get_detail_content(tmp_detail_url, pause=False)
        if detail_content == "":
            return None
        detail_url = MediaPressAdapter.get_detail_url(detail_content)
        CrawlerLogger.logger.info("detail_url: " + detail_url)
        if len(detail_url) == 0:
            CrawlerLogger.logger.warning("error detail_url: " + detail_url)
            CrawlerLogger.logger.warning("detail_content: " + detail_content)
            return None

        finds = re.findall(r'var msg_title = "(.*)"', detail_content)
        if len(finds) == 0:
            CrawlerLogger.logger.warn("ger title str error" + detail_content)
            return None
        title = finds[0]
        CrawlerLogger.logger.info("title: " + title.encode('utf-8'))

        finds = re.findall(r'var msg_desc = "(.*)"', detail_content)
        if len(finds) == 0:
            CrawlerLogger.logger.warn("ger snippet str error" + detail_content)
            return None
        snippet = finds[0]
        CrawlerLogger.logger.info("snippet: " + snippet.encode('utf-8'))

        finds = re.findall(r'var msg_cdn_url = "(.*)"', detail_content)
        if len(finds) == 0:
            CrawlerLogger.logger.warn("ger snippet str error" + detail_content)
            return None
        cover = finds[0]
        CrawlerLogger.logger.info("cover: " + cover)

        finds = re.findall(r'var ct = "(.*)"', detail_content)
        if len(finds) == 0:
            CrawlerLogger.logger.warn("ger snippet str error" + detail_content)
            return None
        published_time = int(finds[0])
        CrawlerLogger.logger.info("published_time: " + str(published_time))

        content_html = etree.HTML(detail_content)
        author = util.get_text(content_html, '//em[@class="rich_media_meta rich_media_meta_text"][last()]', True)
        CrawlerLogger.logger.info("author: " + author)

        doc = Doc(self.source, title, detail_url, snippet, cover, author, self.channel, published_time)

        CrawlerLogger.logger.info("ger latest doc succ" + str(doc))
        return doc


if __name__ == '__main__':
    CrawlerLogger.set_up('logs/crawler.log')
    adapter = MediaPressAdapter(
        seed_url='http://weixin.sogou.com/weixin?type=1&query=non-exist-FAA', channel=u'不存在')
    # adapter = MediaPressAdapter(
    #     seed_url='http://weixin.sogou.com/weixin?type=1&query=almosthuman2014', channel=u"机器之心")
    adapter.get_docs()
    # ls = "http://mp.weixin.qq.com/s?__biz=MzIxNzA0NzM4NA==\x26amp;mid=2651262764\x26amp;idx=1\x26amp;sn=646afdabe920d31f07700abb427eb75a\x26amp;chksm=8c0c671bbb7bee0d319069b5ebabfb86c278cc52ce1dc86e494bebe971d851e92184ad999069#rd"
    # print ls.replace('\x26amp;', '&')


