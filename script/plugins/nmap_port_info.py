#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import subprocess
from script import config
import platform


def nmap_scan(domain):
    global pipe
    if config.nmap_cmd_line == '':
        if platform.architecture()[1] == "WindowsPE":
            cmd = " nmap -sV -sS -T4 --open -O -p-  {0}".format(domain)
        else:
            cmd = " sudo nmap -sV -sS -T4 --open -O -p-  {0}".format(domain)
        try:
            pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
        except Exception as e:
            print(e)
        script_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        finally_path = os.path.join(script_path, 'output/{0}'.format("nmap_info_result.txt"))
        with open(finally_path, "wb") as f:
            f.write(pipe.read())
    else:
        cmd = config.nmap_cmd_line
        try:
            pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
        except Exception as e:
            print(e)
        script_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        finally_path = os.path.join(script_path, 'output/{0}'.format("nmap_info_result.txt"))
        with open(finally_path, "wb") as f:
            f.write(pipe.read())
