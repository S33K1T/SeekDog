#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from script.lib import logger
from script.lib import requests

author = "SpongeB0B"
scope = "dedecms版本探测"
description = "亿邮邮件系统存在弱口令账户信息泄露，导致非法登录"
reference = ""
options = [
    {
        "Name": "URL",
        "Current Setting": "",
        "Required": True,
        "Description": "网站地址"
    }
]

def check_ver(arg):
	ver_histroy = {'20080307': 'v3 or v4 or v5',
			 '20080324': 'v5 above',
			 '20080807': '5.1 or 5.2',
			 '20081009': 'v5.1sp',
			 '20081218': '5.1sp',
			 '20090810': '5.5',
			 '20090912': '5.5',
			 '20100803': '5.6',
			 '20101021': '5.3',
			 '20111111': 'v5.7 or v5.6 or v5.5',
			 '20111205': '5.7.18',
			 '20111209': '5.6',
			 '20120430': '5.7SP or 5.7 or 5.6',
			 '20120621': '5.7SP1 or 5.7 or 5.6',
			 '20120709': '5.6',
			 '20121030': '5.7SP1 or 5.7',
			 '20121107': '5.7',
			 '20130608': 'V5.6-Final',
			 '20130922': 'V5.7SP1'}
	ver_list = sorted(list(ver_histroy.keys()))
	ver_list.append(arg)
	sorted_ver_list=sorted(ver_list)
	return ver_histroy[ver_list[sorted_ver_list.index(arg) - 1]]
		
def exploit(url):
	headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
    			}
	payload = "/data/admin/ver.txt"
	vulnurl = url + payload
	try:
		req = requests.get(vulnurl, headers=headers, timeout=10)
		req.close()
		m = re.search("^(\d+)$", req.content)
		if m:
			logger.success("[+]探测到dedecms版本...(敏感信息)\t时间戳: %s, 版本信息: %s"%(m.group(1), check_ver(m.group(1))))
			return vulnurl
	except:
		logger.error("[-] "+vulnurl+"====>连接超时")
		pass