#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml import etree
import lassie
from model import Doc

#
# - 幻闻
#
# http://www.wcsfa.com/scfbox_list-4.html
#
# - 动态
#
# http://www.wcsfa.com/scfbox_list-41.html
#
# - 星云奖1-5
#
# http://www.wcsfa.com/review_list-11.html
# http://www.wcsfa.com/review_list-12.html
# http://www.wcsfa.com/review_list-13.html
# http://www.wcsfa.com/review_list-14.html
# http://www.wcsfa.com/review_list-15.html
#
# - 科幻世界
#
# http://www.sfw.com.cn/?cat=9
#
# - 幻想文库
#
# - 书
#
# http://www.newstarpress.com/p-65-0.html
#
# - 知乎-星海航纪
#
# https://zhuanlan.zhihu.com/interimm


def get_text(element, pattern, use_text):
    texts = element.xpath(pattern)
    # print len(texts)
    if use_text:
        text = texts[0].text
    else:
        text = texts[0]
    print text
    return text


if __name__ == '__main__':
    print "hello"
    # print lassie.fetch("http://www.sfw.com.cn/?cat=9")
    r = requests.get("http://www.sfw.com.cn/?cat=9")
    if r.status_code == 200:
        html = etree.HTML(r.text)
        # print r.text
        print type(html)

        namespace = '//div[@class="block archive"]/div'
        result = html.xpath(namespace)
        print type(result)
        print type(result[0])
        for item in result[0: -1]:
            print '--------------------'
            # print type(item)
            # print etree.tostring(item)

            title = get_text(item, './/h2/a/@title', False)
            detail_url = get_text(item, './/h2/a/@href', False)
            snippet = get_text(item, './/p', True)
            cover = get_text(item, './/div[@class="block-image"]/a/img/@src', False)
            author = get_text(item, './/span[@class="block-meta"]/span', True)

            # publish_times = item.xpath('//span[@class="block-meta"]/span')
            # print publish_times[0].text

            # doc = Doc(titles[0].encode('utf-8'), detail_urls[0], snippets[0].text.encode('utf-8'), covers[0], authors[0].text)

            # print doc

        # content_list =





