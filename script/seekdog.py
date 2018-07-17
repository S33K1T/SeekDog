#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
# plugin
from script.plugins import APIscan
#import plugins.sql_inject
from script.plugins import xss_check
from script.plugins.robots import get_rebots_info
from script.plugins.nmap_port_info import nmap_scan
from script.plugins.who_is import get_who_page, get_who_is_page
from script.plugins.subdomain import get_sub_info, get_domain_info
from script.plugins.dns_info import dns
from script.plugins.cms_info import CMS
import urllib.request
#===color===
#import plugins.cmd_color_printers


sys.dont_write_bytecode = True  # 不生成pyc文件

VERSION = 2

try:
    if sys.version_info >= (3,0):
        VERSION = 3
        from urllib.request import urlopen
        from urllib.error import URLError
        import json
    # else:
    #     input = raw_input
    #     from urllib2 import urlopen
    #     from urllib2 import URLError
    #     import json
    #     content = "windows环境python2.x环境乱码请先在终端输入chcp 65001再运行程序"
    #     content_unicode = content.decode("utf-8")
    #     content_gbk = content_unicode.encode("gbk")
    #     print (content_gbk)
except:
        pass


def fetch(url, decoding='utf-8'):
    "Fetches content of URL"
    return urlopen(url).read().decode(decoding)

def banner():
    print('                   _       _				    ')
    print('     ___  ___  ___| | ____| | ___   __ _	    ')
    print('    / __|/ _ \/ _ \ |/ / _` |/ _ \ / _` |	')
    print('    \__ \  __/  __/   < (_| | (_) | (_| |	')
    print('    |___/\___|\___|_|\_\__,_|\___/ \__, |	')
    print('                                    |___/	')
    print('\t create by SpongeB0B (1.0.5,2018.4.18)\n')

def menu():
    print ("\n")
    print ("1. whois类信息")
    print ("2. DNS类信息")
    print ("3. 网站安全检测")
    print ("4. 端口扫描")
    print ("5. web指纹")
    print ("6. 蜜罐检测")
    print ("7. robots文件枚举")
    print ("8. 链接检测")
    print ("9. ip定位")
    print ("10.路由跳点")
    print ("11.ping")
    print ("12.反向ip查找")
    print ("13.社会工程学查询")
    print ("14.sql注入检测")
    print ("15.xss漏洞检测")
    print ("16.CVE信息查询")
    print ("退出输入exit")
    print ("\n")

def dog():
    choice = '1'  # Set as default to enter in the loop
    banner()

    while choice != 'exit':
        menu()
        choice = input('选择功能: ')

        if choice == '1':
            APIscan.whois_menu()
            choice1 = input('输入选择的功能:')
            domain = input('输入查询的域名或ip: ')

            if choice1 == '1':
                who = APIscan.whois(domain)
                pwho = fetch(who)
                print(pwho)

            elif choice1 == '2':
                get_who_page(domain)
                print("扫描完成!whois信息已经保存在output/whois1.html文件中！")

            elif choice1 == '3':
                get_who_is_page(domain)
                print("扫描完成!whois信息已经保存在output/whois1.html文件中！")

            elif choice1 == '4':
                beian = APIscan.beian(domain)
                sbeian = fetch(beian)
                json_dict = json.loads(sbeian)
                APIscan.beianjson(json_dict)

        elif choice == '2':
            APIscan.dns_menu()
            choice1 = input('输入你的选择:')
            domain = input('输入查询的域名: ')

            if choice1 == '1':
                dns(domain)
                ns = APIscan.dnscf(domain)
                pns = fetch(ns)
                print("扫描完成!dns信息已经保存在output/dns.html文件中！")
                print(pns)

                if 'cloudflare' in pns:
                    print("检测到子域名!")
                    get_sub_info(domain)
                    print("扫描完成!子域名信息已经保存在output/subdomain.xls文件中！")
                    get_domain_info(domain)
                    print("扫描完成!匹配域名信息已经保存在output/subdoamin.html文件中！")
                else:
                    print("没有发现子域名")

            elif choice1 == '2':
                ns = APIscan.reverse_dns(domain)
                pns = fetch(ns)
                print(pns)

            elif choice1 == '3':
                zone = APIscan.zone(domain)
                pzone = fetch(zone)
                print(pzone)
                if 'failed' in pzone:
                    print("域传送失败")

            else:
                print('[-] 无效的选项!')

        elif choice == '3':
            domain = input('输入目标: ')
            safe = APIscan.webscan(domain)
            fsafe = fetch(safe)
            json_dict = json.loads(fsafe)
            APIscan.webjson(json_dict)

        elif choice == '4':
            domain = input('输入目标的ip地址: ')
            port = APIscan.port(domain)
            pport = fetch(port)
            nmap_scan(domain)
            print("扫描完成!系统和端口信息已经保存在output/nmap_info_result.txt文件中！")
            print(pport)

        elif choice == '5':
            domain = input('输入目标的ip地址: ')
            # header = plugins.APIscan.header(domain)
            # pheader = fetch(header)
            CMS(domain).is_q_empty()
            CMS(domain).set_gevent()
            print("扫描完成!web指纹信息已经保存在output/cms_info.txt文件中！")
            # print(pheader)

        elif choice == '6':
            ip = input('输入ip地址: ')
            honey = APIscan.honey(ip)

            try:
                phoney = fetch(honey)
            except URLError:
                phoney = None
                print('[-] No information available for that IP!')

            if phoney:
                print('Honeypot Probabilty: {probability}%'.format(
                    color='2' if float(phoney) < 0.5 else '3', probability=float(phoney) * 10))

        elif choice == '7':
            domain = input('输入目标: ')
            get_rebots_info(domain)
            print('扫描完成！rebots信息已经保存在output/robots.txt中!')
            robot = APIscan.robot(domain)

            try:
                probot = fetch(robot)
                print(probot)
            except URLError:
                print('[-] Can\'t access to {page}!'.format(page=robot))

        elif choice == '8':
            page = input('输入URL: ')
            crawl = APIscan.crawl(page)
            pcrawl = fetch(crawl)
            print (pcrawl)

        elif choice == '9':
            ip = input('输入IP地址: ')
            geo = APIscan.geo(ip)
            ipcity = APIscan.ipcity(ip)

            try:
                pgeo = fetch(geo)
                pipcity = fetch(ipcity)
                json_dict = json.loads(pgeo)
                APIscan.ipstation(json_dict)
                json_dict = json.loads(pipcity)
                APIscan.city(json_dict)
            except URLError:
                print('[-] 请输入可用的ip地址!')

        elif choice == '10':
            domain = input('输入目标的ip地址: ')
            trace = APIscan.trace(domain)
            ptrace = fetch(trace)
            print (ptrace)

        elif choice == '11':
            domain = input('输入ip或域名:')
            ping = APIscan.nping(domain)
            nping = fetch(ping)
            print (nping)

        elif choice == '12':
            domain = input('输入ip地址')
            reverseip = APIscan.reverse_ip(domain)
            freverseip = fetch(reverseip)
            print (freverseip)

        elif choice == '13':
            APIscan.SET_menu()
            choice1 = input('选择查询的项目：')
            if choice1 == '1':
                domain = input('输入手机号码：')
                phone = APIscan.sphone(domain)
                fphone = fetch(phone)
                json_dict = json.loads(fphone)
                result = json_dict['result']
                print(result)
            elif choice1 == '2':
                domain = input('输入邮箱地址：')
                email = APIscan.email(domain)
                semail = fetch(email)
                json_dict = json.loads(semail)
                APIscan.email_json(json_dict)
            else:
                print('[-] 无效的选项!')

        # elif choice == '14':
        #     url = input('输入检测的url：')
        #     plugins.sql_inject.run(url,'html')

        elif choice == '15':
            url = input("输入检测的url：")
            xss_check.run(url)

        elif choice == '16':
            domain = input("输入CVE编号：")
            cve_info = APIscan.CVE_info(domain)
            fcve_info = fetch(cve_info)
            json_dict = json.loads(fcve_info)
            APIscan.CVE_json(json_dict)

        elif choice == 'exit':
            print('程序退出！！')

        else:
            print('[-] 无效的选项!')
            # except:
            #    print('[-] 发生了错误!')


#******** Main ********#

if __name__ == '__main__':
    dog()
