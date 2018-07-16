#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: SpongeB0B
# Development environment:pycharm 2017.2.3
# Description: __init__.py python2.7+python3.6
#================================项目结构=======================================================
# ├── seekdog.py(主函数)  Main function
# ├── plugins(功能函数目录)  Function function directory
# │   ├── APIscan.py(API函数文件) Store the API function
# │   ├── cmd_color_printers.py(windows彩色终端字体) Modify the color of the font output in the windows cmd
# │   ├── http_request.py(http请求) Two http request get methods and post methods
# │   ├── robots.py(读取rebots信息) Get rebots file information
# │   ├── nmap_port_info.py(辅助工具 Nmap (诸神之眼)) Need to install nmap locally and add it to environment variables
# │   ├── who_is.py(使用who.is和站长之家查询whois信息) Using third-party query target whois
# │   ├── output_html.py(将扫描结果的网页截取保存到本地)Save the scan result web page to local
# │   ├── cms_info.py(web指纹识别) Web fingerprinting
# │   ├── dns_info.py(DNS信息查询) DNS Lookup
# │   ├── subdomain.py(子域名查询) Cloudflare Detector
# ├── config（配置文件） Profile
# │   ├── cms.txt(cms规则文件) Cms rule file
# │   └── config.py(参数配置) Parameter configuration
# ├── output(输出目录) Output directory
# │   ├── whois1.html (whois信息) Whois information
# │   └── whois2.html (whois信息) Whois information
# │   └── rebots.txt (rebots.txt信息) Rebots.txt information
# │   ├── subdomain.xls (子域名信息) Subdomain information
# │   └── subdoamin.html (匹配域名) Match domain name
# │   └── nmap_info_result.txt (系统信息，端口信息等) System information, port information, etc.
# │   └── dns.html (dns信息) DNS information
# ├── static(静态资源目录) Static resource directory
# ├── requirements.txt(依赖库) Dependent library
# └── README.md(说明文档) Documentation
#=============================================================================================
# ================plugin description================
# ==========APIscan.py==============================
# whois() : By api query whois information
# beian() : Web site information
# DNS class security
    # dnscl() : DNS Lookup + Cloudflare Detector
    # reverse_dns() : Reverse DNS resolution
    # zone() : Zone Transfer
# webscan : Testing Website Security via API
# webjson : Handle the json package file returned by the webscan() function and format the display
# port() : Port Scan of nmap
# header() : HTTP Header Grabber
# honey(): Honeypot Detector\
# robots : Robots.txt Scanner
# crawl() : Link Grabber
# geo() : IP Location Finder
# trace() : Traceroute
# nping() : A ping test is used to determine the connectivity and latency of Internet connected hosts
# reverse_ip() : Perform a reverse IP lookup to find all A records associated with an IP address
# Social Engineering Tools
    # sphone() : Telephone inquiries
    # email() : Mailbox status detection
