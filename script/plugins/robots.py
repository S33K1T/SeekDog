#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os

from script.lib.http_request import http_get, is_domain


def get_rebots_info(domain):
    if is_domain(domain):
        try:
            finally_url = "http://" + domain + '/robots.txt'
            result = http_get(finally_url)
            return result
            # script_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
            # finally_path = os.path.join(script_path, 'output/{0}'.format("robots.txt"))
            # if result:
            #     with open(finally_path, 'wb') as f:
            #         f.write(result.encode('utf-8'))
        except Exception as e:
            # print(e)
            return "robots not find"