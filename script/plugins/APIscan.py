#!/usr/bin/env python
# -*- coding:UTF-8 -*-
import json
#=========API KEY============
# http://www.haoservice.com
# 网站安全检测
haoservice_apikey1='eebe71493f64495892646ec88231df7b'
# IP查询
haoservice_apikey2='6bc586e2f9994261b4c0a620f43c27d9'
#手机归属地查询
haoservice_apikey3='ae22e5a8d31947e89169b9754a61697f'
#邮箱地址验证
haoservice_apikey4='4d223a4c76bd42a1933ca8e10a3fb358'
#shodan蜜罐检测
shodan_apikey='C23OXE0bVMrul2YeqcL7zxb6jZ4pj2by'

#===============function===============================
def whois_menu():
    print("1.whois信息查询(hackertarget)")
    print("2.whois信息查询(who.is)")
    print("3.whois信息查询(站长之家)")
    print("4.网站备案数据查询")

def dns_menu():
    print("1.正向DNS解析+子域名枚举")
    print("2.反向DNS解析")
    print("3.DNS域传送")

def SET_menu():
    print("1.手机号码查询")
    print("2.邮箱地址验证")
#whois信息查询
def whois(domain):
    who = "http://api.hackertarget.com/whois/?q=" + domain
    return who
#网站备案查询
def beian(domain):
    bei = "https://www.sojson.com/api/gongan/" + domain
    return bei

def beianjson(json_dict):
    sitename = json_dict['data']['sitename']
    sitetype = json_dict['data']['sitetype']
    sitedomain = json_dict['data']['sitedomain']
    cdate = json_dict['data']['cdate']
    comaddress = json_dict['data']['comaddress']
    comname = json_dict['data']['comname']
    id = json_dict['data']['id']
    print("\n")
    print('简称:',sitename)
    print('网站类型',sitetype)
    print('域名:',sitedomain)
    print('工信部更新时间:',cdate)
    print('公司地址:',comaddress)
    print('公司名称:',comname)
    print('网备编号:',id)
#DNS反向查询
def dnscf(domain):
    ns = "http://api.hackertarget.com/dnslookup/?q=" + domain
    return ns
#DNS正向查询
def reverse_dns(domain):
    redns = "https://api.hackertarget.com/reversedns/?q=" + domain
    return  redns
#DNS域传送
def zone(domain):
    zone = "http://api.hackertarget.com/zonetransfer/?q=" + domain
    return zone
#网站安全查询
def webscan(domain):
    safe = " http://apis.haoservice.com/lifeservice/webscan?domain=" + domain + "&key=" + haoservice_apikey1
    return safe

def webjson(json_dict):
    galevel = json_dict['result']['data']['guama']['level']
    gamsg = json_dict['result']['data']['guama']['msg']
    xjlevel = json_dict['result']['data']['xujia']['level']
    xjmsg = json_dict['result']['data']['xujia']['msg']
    cglevel = json_dict['result']['data']['cuangai']['level']
    cgmsg = json_dict['result']['data']['cuangai']['msg']
    pzlevel = json_dict['result']['data']['pangzhu']['level']
    pzmsg = json_dict['result']['data']['pangzhu']['msg']
    score = json_dict['result']['data']['score']['score']
    result_msg = json_dict['result']['data']['score']['msg']
    google = json_dict['result']['data']['google']['msg']
    ldhigh = json_dict['result']['data']['loudong']['high']
    ldmid = json_dict['result']['data']['loudong']['mid']
    ldlow = json_dict['result']['data']['loudong']['low']
    ldinfo = json_dict['result']['data']['loudong']['info']
    aqlevel = json_dict['result']['webstate']
    if aqlevel == '0':
        aqmsg = '安全'
    elif aqlevel == '1':
        aqmsg = '警告'
    elif aqlevel == '2':
        aqmsg = '严重'
    elif aqlevel == '3':
        aqmsg = '危险'
    else:
        aqmsg = '未知'
    print("\n")
    print('|网站安全等级：' + aqmsg)
    print('|高危漏洞：', ldhigh, '|严重漏洞', ldmid, '|警告漏洞', ldlow, '|提醒漏洞', ldinfo)
    print('|风险等级：', galevel, " |" + gamsg)
    print('|风险等级：', xjlevel, " |" + xjmsg)
    print('|风险等级：', cglevel, " |" + cgmsg)
    print('|风险等级：', pzlevel, " |" + pzmsg)
    print('|安全得分：', score, " |" + result_msg)
    print(google)
#端口扫描
def port(domain):
    port = "http://api.hackertarget.com/nmap/?q=" + domain
    return  port
#web指纹查询
def header(domain):
    header = "http://api.hackertarget.com/httpheaders/?q=" + domain
    return header
#蜜罐检测
def honey(ip):
    honey = "https://api.shodan.io/labs/honeyscore/" + ip + "?key=" + shodan_apikey
    return  honey
#rotbots文件枚举
def robot(domain):
    if not (domain.startswith('http://') or domain.startswith('https://')):
        domain = 'http://' + domain
    robot = domain + "/robots.txt"
    return robot
#链接检测
def crawl(page):
    if not (page.startswith('http://') or page.startswith('https://')):
        page = 'http://' + page
    crawl = "https://api.hackertarget.com/pagelinks/?q=" + page
    return crawl
#IP定位
def geo(ip):
    geo = "http://ipinfo.io/" + ip + "/geo"
    return geo

def ipcity(ip):
    ipcity = " http://apis.haoservice.com/lifeservice/QueryIpAddr/query?ip=" + ip + "&key=" + haoservice_apikey2
    return ipcity

def ipstation(json_dict):
    ip = json_dict['ip']
    loc = json_dict['loc']
    print('IP地址：',ip)
    print('IP定位的经纬度:',loc)

def city(json_dict):
    city = json_dict['result']['city']
    isp = json_dict['result']['isp']
    district = json_dict['result']['district']
    print('城市：', city)
    print('区（县）：',district)
    print('Internet服务提供者：', isp)
#路由跳点
def trace(domain):
    trace = "https://api.hackertarget.com/mtr/?q=" + domain
    return  trace
#ping
def nping(domain):
    ping = "https://api.hackertarget.com/nping/?q=" + domain
    return  ping
#反向IP查找
def reverse_ip(domain):
    reverseip = "https://api.hackertarget.com/reverseiplookup/?q=" + domain
    return  reverseip
#CVE编号查询
def CVE_info(domain):
    cve_info = "http://cve.circl.lu/api/cve/" + domain
    return cve_info

def CVE_json(json_dict):
    modified = json_dict['Modified']
    published = json_dict['Published']
    complexity = json_dict['access']['complexity']
    vector = json_dict['access']['vector']
    authentication = json_dict['access']['authentication']
    cvss = json_dict['cvss']
    cvss_time = json_dict['cvss-time']
    cwe = json_dict['cwe']
    confidentiality = json_dict['impact']['confidentiality']
    availability = json_dict['impact']['availability']
    integrity = json_dict['impact']['integrity']
    # nessus = json.dumps(json_dict['nessus'], indent=1)
    summary = json_dict['summary']
    vulnerable_configuration_cpe_2_2 = json.dumps(json_dict['vulnerable_configuration_cpe_2_2'],indent=1)
    vulnerable_configuration = json.dumps(json_dict['vulnerable_configuration'],indent=1)
    print('发布日期：',published)
    print('更新日期：', modified)
    print('*******************CVSS (基础分值)************************************')
    print('cvss更新时间：', cvss_time)
    print('CVSS分值：',cvss)
    cvss = float(cvss)
    if cvss < 4.0:
        print('危险等级：低！')
    elif 4.0 <= cvss < 7.0:
        print('危险等级：中！')
    else:
        print('危险等级：高！')
    print('机密性影响：',confidentiality)
    print('可用性影响：', availability)
    print('完整性影响：',integrity)
    print('攻击复杂度：', complexity)
    print('攻击向量：',vector)
    print('身份认证：',authentication)
    print('CWE (弱点类目)：',cwe)
    print('CPE (受影响的平台与产品)：\n', vulnerable_configuration_cpe_2_2)
    print('*********************漏洞信息*****************************************')
    print('CVE简介：', summary)
    print('受影响的程序版本：',vulnerable_configuration)
    # print('nessus:',nessus)
    print('CAPEC常见攻击模式的枚举与分类')
    for i in range(0, len(json_dict['capec'])):
        name = json_dict['capec'][i]['name']
        prerequisites = json_dict['capec'][i]['prerequisites']
        solutions = json_dict['capec'][i]['solutions']
        capec_summary = json_dict['capec'][i]['summary']
        print('CVE名字：', name)
        print('先决条件：', prerequisites)
        print('解决方案：', solutions)
        print('简介：', capec_summary)
        print('========================================================================================\n')

#SET tools API
#手机归属地查询
def sphone(domain):
    phone = "http://apis.haoservice.com/mobile?phone=" + domain + "&key=" + haoservice_apikey3
    return phone
#邮箱检测
def email(domain):
    email = "http://apis.haoservice.com/lifeservice/VerifyEmail?email=" + domain + "&key=" + haoservice_apikey4
    return email

def email_json(json_dict):
    sstatus = json_dict['result']['status']
    status_info = json_dict['result']['status_info']
    if sstatus == '0':
        print("邮箱状态：不可用！")
    else:
        print("邮箱状态：正常！")
    print('邮箱状态描述:',status_info)