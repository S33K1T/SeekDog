#!/usr/bin/env python  
# -*- encoding: utf-8 -*-
'''
功能：whois信息查找
输入：url或ip
输出：whois1.html或whois2.html
'''
import os
import re

import requests
from bs4 import BeautifulSoup

from script.config import config
from script.lib.http_request import http_get, http_post, is_domain
from script.lib.output_html import out_page

if config.allow_http_session:
    requests = requests.Session()

def get_who_page(domain):

    if is_domain(domain):
        url = "https://who.is/whois/{0}".format(domain)
        try:
            web_content = http_get(url)
            bs = BeautifulSoup(web_content, "html.parser")
            result = bs.find("div", class_="col-md-8")
            rule = re.compile('(\/tools\/)')
            finally_result = rule.sub('https://who.is//tools/', result.prettify())
            script_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
            finally_path = os.path.join(script_path, 'output/{0}'.format("whois1.html"))
            sty = '<head><meta charset="UTF-8"><link href="../static/Bootstrap.css" rel="stylesheet" ' \
                  'type="text/css" /><link href="../static/main.css" rel="stylesheet" type="text/css" /></head>'
            out_page(finally_path, sty, finally_result)

        except Exception as e:
            print(e)


def get_who_is_page(domain):
    if is_domain(domain):
        url = "http://whois.chinaz.com/{0}".format(domain)
        payload = {
            'DomainName': domain
        }
        try:
            content = http_post(url, payload)
            bs = BeautifulSoup(content, 'html.parser')
            ul = bs.find('ul', class_="WhoisLeft")
            if ul is not None:
                script_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
                finally_path = os.path.join(script_path, '..\\templates\\output\\{0}'.format("whois2.html"))
                sty = '<head><meta charset="UTF-8"> <link rel="stylesheet" href="../../static/css/whois.css"> ' \
                    '<link rel="stylesheet" href="../../static/css/whois_base.css"></head>'
                out_page(finally_path, sty, ul.prettify())
        except Exception as e:
            print(e)
