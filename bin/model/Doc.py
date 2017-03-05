#!/usr/bin/env python
# -*-coding:utf-8-*-
import time


class Doc:
    def __init__(self, source, title, detail_url, snippet, cover, author, channel, publish_time=time.time(),
                 create_time=None, update_time=None):
        self.source = source
        self.title = title
        self.detail_url = detail_url
        self.snippet = snippet
        self.cover = cover
        self.publish_time = publish_time
        self.channel = channel
        self.author = author
        self.docid = hash(detail_url)
        self.create_time = create_time
        self.update_time = update_time
        self.publish_str = time.strftime("%Y年%m月%d日", time.localtime(publish_time))

    def __str__(self):
        return "docid: {0}\ntitle: {1}\ndetail_url: {2}\nsnippet: {3}\ncover: {4}\nauthor: {5}\n" \
               "channel: {6}\nsource: {7}\npublish_time: {8}\ncreate_time: {9}\npublished_time: {10}".format(
                self.docid, self.title.encode('utf-8'), self.detail_url, self.snippet.encode('utf-8'), self.cover,
                self.author.encode('utf-8'), self.channel.encode('utf-8'), self.source.encode('utf-8'),
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.publish_time)),
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.create_time)) if self.create_time else "None",
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.update_time)) if self.update_time else "None")

    @staticmethod
    def to_doc(doc_row):
        publish_time = int(time.mktime(doc_row.get('publishTime', None).timetuple()) + 8 * 3600)

        return Doc(doc_row.get('source', None), doc_row.get('title', None), doc_row.get('detailUrl', None),
                   doc_row.get('snippet', None), doc_row.get('cover', None), doc_row.get('author', None),
                   doc_row.get('channel', None), publish_time,
                   time.mktime(doc_row.get('createTime', None).timetuple()) + 8 * 3600,
                   time.mktime(doc_row.get('updateTime', None).timetuple()) + 8 * 3600)

    @staticmethod
    def to_docs(doc_rows):
        docs = list()
        for doc_raw in doc_rows:
            docs.append(Doc.to_doc(doc_raw))
        return docs

if __name__ == '__main__':
    print hash("aaaaa")
    print hash("aaaab")


