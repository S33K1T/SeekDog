#!/usr/bin/env python
#-*- coding:utf-8 -*-

from script.lib import downloader,common
import os

payload = []
script_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
finally_path = os.path.join(script_path, 'data/{0}'.format("xss.txt"))
f = open(finally_path)
for i in f:
    payload.append(i.strip())

def run(url):
    download = downloader.HtmlDownloader()
    urls = common.urlsplit(url)
    if urls is None:
        return False
    for _urlp in urls:
        for _payload in payload:
            _url = _urlp.replace("my_Payload",_payload)
            #我们需要对URL每个参数进行拆分,测试
            _str = download.request(_url)
            if _str is None:
                return False
            if(_str.find(_payload)!=-1):
                return "xss found:%s"%_url
    return False

