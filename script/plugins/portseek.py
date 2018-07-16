#!/usr/bin/env python
# coding=utf-8

import re
import json
import os
from queue import Queue
from threading import Thread
from telnetlib import Telnet

title = ""
result = []

#默认常用端口介绍：
def PORT_enum():
    print("默认常用端口介绍:")
    print('*' * 64)
    PORT={80:"web",8080:"web",3311:"kangle主机管理系统",3312:"kangle主机管理系统",3389:"远程登录",4440:"rundeck是用java写的开源工具",5672:"rabbitMQ",5900:"vnc",6082:"varnish",7001:"weblogic",8161:"activeMQ",8649:"ganglia",9000:"fastcgi",9090:"ibm",9200:"elasticsearch",9300:"elasticsearch",9999:"amg",10050:"zabbix",11211:"memcache",27017:"mongodb",28017:"mondodb",3777:"大华监控设备",50000:"sap netweaver",50060:"hadoop",50070:"hadoop",21:"ftp",22:"ssh",23:"telnet",25:"smtp",53:"dns",123:"ntp",161:"snmp",8161:"snmp",162:"snmp",389:"ldap",443:"ssl",512:"rlogin",513:"rlogin",873:"rsync",1433:"mssql",1080:"socks",1521:"oracle",1900:"bes",2049:"nfs",2601:"zebra",2604:"zebra",2082:"cpanle",2083:"cpanle",3128:"squid",3312:"squid",3306:"mysql",4899:"radmin",8834:'nessus',4848:'glashfish'}
    ident = PORT
    for i in ident.keys():
        print(i,ident[i])
    print('*' * 64)

class PortSeek(Thread):
    TIMEOUT = 6  # 默认扫描超时时间

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def auth(self, url):
        host = url.split(':')[0]
        port = url.split(':')[-1]

        try:
            tn = Telnet(host=host, port=port, timeout=self.TIMEOUT)
            tn.set_debuglevel(9)
            #print('[*] ' + url + ' ---> open')

            with open(os.path.dirname(__file__) + "/../output/port_result.txt", 'a') as f:
                try:
                    f.write(str('[*]'+url) + '\n')
                except:
                    pass
        except Exception as e:
            pass
        finally:
            tn.close()

    def run(self):
        while not self.queue.empty():
            url = self.queue.get()
            try:
                self.auth(url)
            except:
                continue


def dispatcher(ip_file=None, ip=None, max_thread=100, portlist=None):
    iplist = []
    for _ip in ip:
        iplist.append(_ip)

    with open(os.path.dirname(__file__) + "/../output/port_result.txt", 'w'):
        pass

    q = Queue()
    for ip in iplist:
        for port in portlist:
            url = str(ip) + ':' + str(port)
            q.put(url)

    title = ('队列大小：' + str(q.qsize()))

    threadl = [PortSeek(q) for _ in range(max_thread)]
    for t in threadl:
        t.start()

    for t in threadl:
        t.join()

    return  title

def run(ip, max_threads=30):
    print("输入ip地址和域名都能扫描，请尽量使用ip地址，除非确认此域名没有waf或CDN！\n")
    print("默认配置可以为空，如果批量扫描，请输入目标地址列表的文件名（指定存放ip的文件，每一行一个ip或域名）！\n")
    print("指定扫描端口，支持三种格式：(1)80  (2)80,443,3306,3389  (3)1-65535 (如果不指定将按照默认端口扫描)\n")

    print('-' * 64)

    portlist = [21, 22, 23, 53, 80, 111, 139, 161, 389, 443, 445, 512, 513, 514,
                873, 1025, 1433, 1521, 3128, 3306, 3311, 3312, 3389, 5432, 5900,
                5984, 6082, 6379, 7001, 7002, 8000, 8080, 8081, 8090, 9000, 9090,
                8888, 9200, 9300, 10000, 11211, 27017, 27018, 50000, 50030, 50070]
    print('不指定端口，将只扫描已经设置了默认的端口!')

    if ip:
        try:
            dispatcher(ip=ip, max_thread=max_threads, portlist=portlist)
        except Exception as e:
            print(e)
    else:
        print("请指定IP地址或域名和端口进行扫描！")

def txt2json():
    # 你的文件路径
    path = os.path.dirname(__file__) + "/../output/port_result.txt"
    # 读取文件
    file = open(path, encoding="utf-8")
    # 定义一个用于切割字符串的正则
    seq = re.compile(":")

    result = []
    # 逐行读取
    for line in file:
        lst = seq.split(line.strip())
        item = {
            "ip": lst[0],
            "port": lst[1:]
        }
        result.append(item)
    # 关闭文件
    file.close()
    return json.dumps(result)

if __name__ == '__main__':
    run(['www.qqyewu.com','www.baidu.com'])
    txt2json()


