#!/usr/bin/env python
# -*-coding:utf-8-*-
import time
import datetime


class Seed:
    def __init__(self, url, adapter, freq_min=60, last_time=time.time(), seed_id=None, source="", channel="", status=1):
        self.url = url
        self.adapter = adapter
        self.freq_min = freq_min
        self.last_time = last_time
        self.next_time = last_time + self.freq_min * 60
        self.id = seed_id
        self.source = source
        self.channel = channel
        self.status = status

    def __str__(self):
        return "url: {0}\nfreq_min: {1}\nlast_time: {2}\nadapter: {3}\nid: {4}\nnext_time: {5}\n" \
               "source: {6}\nchannel: {7}\nstatus: {8}".format(
                self.url, self.freq_min,
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.last_time)),
                self.adapter, self.id,
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.next_time)),
                self.source.encode('utf-8'), self.channel.encode('utf-8'), self.status)

    @staticmethod
    def to_seed(seed_row):
        return Seed(seed_row.get('url', None), seed_row.get('adapter', None), seed_row.get('freqMin', None),
                    time.mktime(seed_row.get('lastTime', None).timetuple()) + 8 * 3600,
                    seed_row.get('id', None), seed_row.get('source', ""), seed_row.get('channel', ""),
                    seed_row.get('status', 0))

    @staticmethod
    def to_seeds(seed_rows):
        seeds = list()
        for seed_raw in seed_rows:
            seeds.append(Seed.to_seed(seed_raw))
        return seeds

if __name__ == '__main__':
    print hash("aaaaa")
    print hash("aaaab")
    dt_obj = datetime.datetime(2008, 11, 10, 17, 53, 59)
    time_tuple = dt_obj.timetuple()
    ts = time.mktime(time_tuple)

    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))



