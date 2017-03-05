#!/usr/bin/env python
# -*- coding:utf-8 -*-

from lxml import etree
from model import Doc
import time

if __name__ == '__main__':
    text = '''
    <div>
        <ul>
             <li class="item-0"><a href="link1.html">first item</a></li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-inactive"><a href="link3.html">third item</a></li>
             <li class="item-1"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a>
         </ul>
     </div>
    '''
    html = etree.HTML(text)

    print type(html)
    result = html.xpath('//ul')
    print(result)
    print(etree.tostring(result[0]))

    result = html.xpath('//li/a')
    for rr in result:
        print rr
        print(rr.text)
        print(rr.attrib.get("href", None))


