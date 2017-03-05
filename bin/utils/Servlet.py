# !/usr/bin/python
# -*- coding: utf-8 -*-
import cookielib
import httplib
import logging
import os
import urllib
import urllib2
import time

__author__ = 'pudding'


class Config(object):
    """
    用于 fetch 连接 url 的一些常数
    """
    RETRY = 3
    TIMEOUT = 30
    USER_AGENT = {"User-Agent": "Mozilla/5.0 Firefox/3.5",
                  "Content-Type": "application/json"}

    INTERVAL = 1


class Servlet(object):
    def __init__(self):
        pass

    @staticmethod
    def try_request(request):
        resp = None
        for i in range(0, Config.RETRY):
            try:
                resp0 = urllib2.urlopen(request)

                resp = resp0.read()
                return resp
            except (urllib2.URLError, urllib2.HTTPError, httplib.BadStatusLine) as ex:
                if i == Config.RETRY - 1:
                    logging.warn("fetch error[{0}], url[{1}], data[{2}]".format(
                        ex, request.get_full_url, request.get_data))
        return resp

    @staticmethod
    def get(url, cookie=False):
        return Servlet.get(url, None, cookie)

    @staticmethod
    def get(url, data=None, cookie=False):
        ## sleep for robot
        """

        :rtype : object
        """
        time.sleep(Config.INTERVAL)
        if cookie:
            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)
        if data is None:
            request = urllib2.Request(url=url, headers=Config.USER_AGENT)
        else:
            assert type(data) is dict
            request = urllib2.Request(url=url + '?' + urllib.urlencode(data), headers=Config.USER_AGENT)
        request.get_method = lambda: "GET"
        resp = Servlet.try_request(request)
        if not resp:
            logging.warn("error to fetch: {0}".format(url))
        return resp

    @staticmethod
    def post(url, data, cookie=False):
        # assert type(data) is dict
        ## sleep for robot
        time.sleep(Config.INTERVAL)
        if cookie:
            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)
        request = urllib2.Request(url=url, data=urllib.urlencode(data), headers=Config.USER_AGENT)
        request.get_method = lambda: "POST"
        return Servlet.try_request(request)

    @staticmethod
    def post_data(url, data, cookie=False):
        # assert type(data) is dict
        ## sleep for robot
        time.sleep(Config.INTERVAL)
        if cookie:
            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)
        request = urllib2.Request(url=url, data=data, headers=Config.USER_AGENT)
        request.get_method = lambda: "POST"
        return Servlet.try_request(request)

    @staticmethod
    def delete(url, cookie=False):
        if cookie:
            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)
        request = urllib2.Request(url=url, headers=Config.USER_AGENT)
        request.get_method = lambda: "DELETE"
        return Servlet.try_request(request)

    @staticmethod
    def curl(url, options=None):
        time.sleep(Config.INTERVAL)
        request_cmd = "curl \"{0}\"".format(url)
        for i in range(0, Config.RETRY):
            try:
                resp = os.popen(request_cmd).read()
                return resp
            except:
                if i == Config.RETRY - 1:
                    logging.warn("curl error url[{0}]".format(url))
        return None
