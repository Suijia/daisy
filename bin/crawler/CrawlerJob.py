#!/usr/bin/env python
# -*-coding:utf-8-*-
import os
import random
import time

from SeedDao import SeedDao
from DocDao import DocDao
from utils.CrawlerLogger import CrawlerLogger
from utils.MysqlLogger import MysqlLogger
from apscheduler.schedulers.background import BackgroundScheduler
from crawler.adapter import *  # 这一行不能删除
from model import Seed
import util
__author__ = 'yangxj'

# ==============================
# author: yangxj
# created at: 16/8/7 下午11:30
# filename: CrawlerJob.py
# ==============================


class CrawlerJob:
    scheduler = BackgroundScheduler()

    def __init__(self):
        self.freq_min = 10

    @staticmethod
    def set_up():
        CrawlerJob.scheduler.add_job(CrawlerJob.first_job, 'interval', seconds=1, id='first_job')
        CrawlerJob.scheduler.add_job(CrawlerJob.job_test, 'interval', seconds=120)
        CrawlerJob.scheduler.start(paused=False)

    @staticmethod
    def job():
        print "I'm working..."
        CrawlerLogger.logger.info("working: ")

    @staticmethod
    def first_job():
        CrawlerLogger.logger.info("first working: ")
        CrawlerJob.scheduler.remove_job('first_job')
        CrawlerJob.schedule()
        CrawlerJob.scheduler.add_job(CrawlerJob.schedule, 'interval', minutes=30)

    @staticmethod
    def job_test():
        CrawlerLogger.logger.info("job test")

    @staticmethod
    def schedule():
        CrawlerLogger.logger.info(">>>>>>>>>>>>>>>>>>>>>>>>>begin schedule")
        try:
            seed_dao = SeedDao()
            doc_dao = DocDao()
            seeds = seed_dao.get_online_seeds()
            for seed in seeds:
                CrawlerJob.crawler_one_seed(seed, doc_dao, seed_dao)
        except Exception as e:
            print e
            CrawlerLogger.logger.info("schedule Exception")
        CrawlerLogger.logger.info("<<<<<<<<<<<<<<<<<<<<<<<<this schedule done ")

    @staticmethod
    def schedule_one_seed(seed_id):
        seed = SeedDao().get_seed(seed_id)
        CrawlerJob.crawler_one_seed(seed)

    @staticmethod
    def crawler_one_seed(seed, doc_dao=DocDao(), seed_dao=SeedDao(), update=False):
        use_time = random.randint(300, 700)   # 每个种子10分钟左右
        start_time = int(time.time())
        if not isinstance(seed, Seed):
            CrawlerLogger.logger.error('doc type error'.format(type(seed)))
            return False
        CrawlerLogger.logger.info("schedule: " + str(seed))
        if seed.next_time < time.time():
            CrawlerLogger.logger.info("begin:++++++++++++++++++ " + seed.url)
            # print globals()
            if seed.adapter not in globals():
                CrawlerLogger.logger.error("adapter {0} should be import".format(seed.adapter))
                return False
            adapter = globals()[seed.adapter](seed.url, seed.source, seed.channel)
            try:
                docs = adapter.get_docs()
                if len(docs) > 0:
                    doc_dao.db.reconnect()
                    succ = doc_dao.insert_docs(docs, update=update)
                    CrawlerLogger.logger.info("insert doc succ: {0} failed: {1}".format(succ, len(docs) - succ))
                    end_time = int(time.time())
                    seed_dao.update_seed_last_time(seed.id, seed.next_time, seed.freq_min)
                    util.print_sleep(use_time - (end_time - start_time), 20, "wait for next seed")
                    return True
                else:
                    CrawlerLogger.logger.error("get doc failed" + seed.url)
            except Exception as e:
                CrawlerLogger.logger.error("get docs failed Exception" + e.message)
        else:
            CrawlerLogger.logger.info("-------------------------->pass next time: " +
                               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(seed.next_time)))
            return False

if __name__ == '__main__':
    CrawlerLogger.set_up('logs/crawler_job.log')
    MysqlLogger.set_up('logs/mysql.log')
    job = CrawlerJob()
    job.schedule_one_seed(9)


    # job.set_up()
    # print "ok"
    #
    # print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    # try:
    #     # This is here to simulate application activity (which keeps the main thread alive).
    #     while True:
    #         time.sleep(2)  # 其他任务是独立的线程执行
    #     print('sleep!')
    # except (KeyboardInterrupt, SystemExit):
    #     # Not strictly necessary if daemonic mode is enabled but should be done if possible
    #     print('Exit The Job!')
