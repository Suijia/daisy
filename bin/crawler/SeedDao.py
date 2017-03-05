#!/usr/bin/env python
# -*-coding:utf-8-*-
import time
import torndb
import yaml
from utils.CrawlerLogger import CrawlerLogger
from utils.MysqlLogger import MysqlLogger
from model import Seed

__author__ = 'yangxj'

# ==============================
# author: yangxj
# created at: 16/8/7 上午9:55
# filename: SeedDao.py
# ==============================


class SeedDao:
    def __init__(self):
        conf = yaml.load(open('conf/service.yaml', 'r'))
        self.db = torndb.Connection(
            host=str(conf['database']['host']) + ':' + str(conf['database']['port']),
            database=str(conf['database']['database']),
            user=str(conf['database']['username']),
            password=str(conf['database']['password']))
        CrawlerLogger.logger.info("connect {0} {1}".format(self.db.host, self.db.database))
        MysqlLogger.logger.info("connect {0} {1}".format(self.db.host, self.db.database))

    def get_all_seeds(self):
        sql = 'SELECT * FROM seed'
        CrawlerLogger.logger.info('get: ' + sql)
        MysqlLogger.logger.info('get: ' + sql)
        seed_rows = self.db.query(sql)
        seeds = Seed.to_seeds(seed_rows)
        return seeds

    def get_online_seeds(self):
        seeds = self.get_all_seeds()
        seeds = filter(lambda x: x.status == 1, seeds)
        return seeds

    def get_seed(self, seed_id):
        sql = 'select * from seed where id=%s'
        sql_str = sql % seed_id
        CrawlerLogger.logger.info('get: {0}\n'.format(sql_str))
        MysqlLogger.logger.info('get: {0}\n'.format(sql_str))
        seed_row = self.db.get(sql, seed_id)
        if seed_row:
            return Seed.to_seed(seed_row)
        return None

    def update_seed_last_time(self, seed_id, last_time=time.time(), freq_min=1440):
        try_time = 0
        while try_time < 3:
            while last_time + freq_min * 60 < time.time():
                last_time += freq_min * 60
            last_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(last_time))
            update_sql = "update seed set lastTime='{0}' where id='{1}'".format(last_time, seed_id)
            CrawlerLogger.logger.info('update seed query ' + update_sql)
            MysqlLogger.logger.info('update seed query ' + update_sql)

            try:
                rows = self.db.update(update_sql)
                if rows == 0:
                    CrawlerLogger.logger.error('update error {0}'.format(seed_id))
                    MysqlLogger.logger.error('update error {0}'.format(seed_id))
                return rows > 0
            except Exception as e:
                CrawlerLogger.logger.error('update seed {0} failed\n'.format(seed_id) + str(e))
                MysqlLogger.logger.error('update seed {0} failed\n'.format(seed_id) + str(e))
                self.db.reconnect()
                try_time += 1


if __name__ == '__main__':
    CrawlerLogger.set_up('logs/crawler.log')
    MysqlLogger.set_up('logs/mysql.log')
    dao = SeedDao()

    seeds_tmp = dao.get_online_seeds()
    for seed in seeds_tmp:
        print seed

