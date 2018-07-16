#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import hashlib
from script.lib import logger
from script.lib import requests

author = "SpongeB0B"
scope = "Discuz X3"
description = "/static/image/common/focus.swf Flash XSS"
reference = ""
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
	flash_md5 = "c16a7c6143f098472e52dd13de85527f"
	payload = "/static/image/common/focus.swf"
	vulnurl = url + payload
	req = urllib.request.urlopen(vulnurl)
	data = req.read()
	md5_value = hashlib.md5(data).hexdigest()
	if md5_value in flash_md5:
		logger.success("[+]存在discuz X3 focus.swf flashxss漏洞...(高危)\tpayload: "+vulnurl)
		return vulnurl