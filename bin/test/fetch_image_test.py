#!/usr/bin/env python
# -*-coding:utf-8-*-
import requests

__author__ = 'yangxj'

# ==============================
# author: yangxj
# created at: 16/8/9 上午11:07
# filename: fetch_image_test.py
# ==============================


def downloadImageFile(imgUrl):
    local_filename = imgUrl.split('/')[-1]
    print "Download Image File=", local_filename
    r = requests.get(imgUrl, stream=True)  # here we need to set stream = True parameter
    with open("/home/pandy/" + local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()
    return local_filename

if __name__ == '__main__':
    downloadImageFile()
