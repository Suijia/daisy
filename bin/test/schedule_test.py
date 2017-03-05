#!/usr/bin/env python
# -*-coding:utf-8-*-

# from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler


def my_job():
    print 'hello world'

if __name__ == '__main__':

    sched = BackgroundScheduler()
    sched.add_job(my_job, 'interval', seconds=1)
    sched.start()
    print "0k"


