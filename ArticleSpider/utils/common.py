#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/4 14:51
# @Author  : shenyoujian
# @description :

import hashlib


# 图片url的md5处理
def get_md5(url):
    # str就是unicode了.Python3中的str对应2中的Unicode
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()