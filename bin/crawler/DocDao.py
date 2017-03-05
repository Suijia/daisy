#!/usr/bin/env python
# -*-coding:utf-8-*-
import time
import torndb
import yaml
from utils.CrawlerLogger import CrawlerLogger
from utils.MysqlLogger import MysqlLogger
from model import Doc

__author__ = 'yangxj'

# ==============================
# author: yangxj
# created at: 16/8/7 上午9:55
# filename: DocDao.py
# ==============================

# CREATE TABLE `doc` (
#   `docid` bigint(20) NOT NULL,
#   `title` varchar(256) DEFAULT NULL,
#   `snippet` text,
#   `cover` varchar(512) DEFAULT NULL,
#   `detailUrl` varchar(512) DEFAULT NULL,
#   `author` varchar(64) DEFAULT NULL,
#   `publishTime` timestamp NULL DEFAULT NULL,
#   `publishStr` varchar(64) DEFAULT NULL,
#   `createTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
#   `updateTime` timestamp NULL DEFAULT NULL,
#   `source` varchar(64) DEFAULT NULL,
#   PRIMARY KEY (`docid`),
#   UNIQUE KEY `docid_UNIQUE` (`docid`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


class DocDao:
    def __init__(self):
        conf = yaml.load(open('conf/service.yaml', 'r'))
        self.db = torndb.Connection(
            host=str(conf['database']['host']) + ':' + str(conf['database']['port']),
            database=str(conf['database']['database']),
            user=str(conf['database']['username']),
            password=str(conf['database']['password']))
        CrawlerLogger.logger.info("connect {0} {1}".format(self.db.host, self.db.database))
        MysqlLogger.logger.info("connect {0} {1}".format(self.db.host, self.db.database))

    def insert_docs(self, docs, update=False):
        succ = 0
        for doc in docs:
            if self.insert_one_doc(doc, update):
                succ += 1
        return succ

    def insert_one_doc(self, doc, update=False):
        # print type(doc)
        # print isinstance(doc, Doc)
        if not isinstance(doc, Doc):
            CrawlerLogger.logger.error('doc type error'.format(type(doc)))
            return False

        if doc.detail_url == "":
            CrawlerLogger.logger.error('doc detail url is empty'.format(str(doc)))
            return False

        if self.is_exist(doc.docid):
            if update:
                return self.update_one_doc(doc)
            else:
                CrawlerLogger.logger.error('doc exist {0}'.format(doc.docid))
                return False

        doc.title = doc.title.replace('&nbsp;', ' ')
        doc.snippet = doc.snippet.replace('&nbsp;', ' ')

        sql = 'insert into doc(docid, title, snippet, cover, detailUrl, author,' \
              'channel, source, updateTime, publishTime) values (%s, %s, %s, %s, %s, %s, %s ,%s, %s, %s)'

        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
        publish_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(doc.publish_time))

        sql_str = sql % (doc.docid, doc.title, doc.snippet, doc.cover, doc.detail_url, doc.author,
                         doc.channel, doc.source, update_time, publish_time)
        CrawlerLogger.logger.info('insert query ' + sql_str)
        MysqlLogger.logger.info('insert query ' + sql_str)
        try:
            self.db.insert(sql, doc.docid, doc.title.encode('utf-8'), doc.snippet.encode('utf-8'),
                           doc.cover.encode('utf-8'), doc.detail_url.encode('utf-8'), doc.author.encode('utf-8'),
                           doc.channel, doc.source.encode('utf-8'), update_time, publish_time)
            return True
        except Exception as e:
            CrawlerLogger.logger.error('insert dod {0} failed\n'.format(sql) + str(e))
            MysqlLogger.logger.error('insert dod {0} failed\n'.format(sql) + str(e))

    def update_one_doc(self, doc):
        if not isinstance(doc, Doc):
            CrawlerLogger.logger.error('doc type error'.format(type(doc)))
            return False

        doc.title = doc.title.replace('&nbsp;', ' ')
        doc.snippet = doc.snippet.replace('&nbsp;', ' ')

        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
        update_sql = "update doc set title='{0}', snippet='{1}', cover='{2}', detailUrl='{3}', author='{4}'," \
                     "channel='{5}', source='{6}',updateTime='{7}' where docid='{8}'".format(
                      doc.title.encode('utf-8'), doc.snippet.encode('utf-8'), doc.cover.encode('utf-8'),
                      doc.detail_url.encode('utf-8'), doc.author.encode('utf-8'), doc.channel.encode('utf-8'),
                      doc.source.encode('utf-8'), update_time, doc.docid)
        CrawlerLogger.logger.info('update query ' + update_sql)
        MysqlLogger.logger.info('update query ' + update_sql)

        try:
            rows = self.db.update(update_sql)
            if rows == 0:
                CrawlerLogger.logger.error('update error {0}'.format(str(doc)))
                MysqlLogger.logger.error('update error {0}'.format(str(doc)))
            return rows > 0
        except Exception as e:
            CrawlerLogger.logger.error('update doc {0} failed\n'.format(update_sql) + str(e))
            MysqlLogger.logger.error('update doc {0} failed\n'.format(update_sql) + str(e))

    def is_exist(self, docid):
        return self.get_doc(docid) is not None

    def get_doc(self, docid):
        sql = 'select * from doc where docid=%s'
        sql_str = sql % docid
        CrawlerLogger.logger.info('get: {0}\n'.format(sql_str))
        MysqlLogger.logger.info('get: {0}\n'.format(sql_str))
        doc_row = self.db.get(sql, docid)
        if doc_row:
            return Doc.to_doc(doc_row)
        return None

    def get_docs(self, source=None, channel=None, start=0, page_size=10):
        sql = 'SELECT * FROM doc'

        wheres = list()
        if source:
            wheres.append("source='" + source + "'")
        if channel:
            wheres.append("channel='" + channel + "'")

        if len(wheres) > 0:
            sql += " WHERE " + " AND ".join(wheres)

        sql += " ORDER BY publishTime DESC LIMIT {0},{1}".format(start, page_size)
        CrawlerLogger.logger.info('get ' + sql)
        MysqlLogger.logger.info('get ' + sql)
        doc_rows = self.db.query(sql)
        docs = Doc.to_docs(doc_rows)
        return docs

if __name__ == '__main__':
    CrawlerLogger.set_up('logs/crawler.log')
    MysqlLogger.set_up('logs/mysql.log')
    dao = DocDao()
    # doc_tmp = Doc(u"这里标题", u"这里标题", "detail_url5", u"这里标题", "cover", "author", u"这里标题")
    # dao.insert_one_doc(doc_tmp)

    docs_tmp = dao.get_docs(source=u'科幻世界')
    print len(docs_tmp)
    for doc_tmp in docs_tmp:
        print "---------------------------"
        print doc_tmp

