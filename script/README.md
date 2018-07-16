#seekdog

----------

## Description

**seekdog**是一款收集CMS、WHOIS 、DNS、robots.txt、子域名、端口信息、系统信息、服务信息的工具。

（Stealth is a tool for collecting CMS, WHOIS, DNS, robots.txt, subdomains, port information, system information, and service information.）
![](https://i.imgur.com/1jtG1tv.png)

----------
##0x01 需求分析
![需求分析.png](https://i.imgur.com/R042LSb.png)
###<font color=red>0x00 平台选择</font>

大部分工具都是寄生在 `Linux` 平台下，这里也打算适应`windows`平台。很多用`python`开发的安全脚本都是基于`Python2.x`的环境开发的，但是未来主流必定是`python3`,这里运行环境兼容`python2.x`和`python3.x`环境。

###<font color=red>0x01	功能需求</font>
    
>1、whois 信息

>2、DNS 记录

>3、端口状态

>4、子域名

>5、主机系统信息

>6、Robots.txt

>7、服务信息

>8、指纹识别

##0x02 资源整合

进行信息收集的功能无可避免会借用到网站资源或者辅助工具。网站资源指的是搜索引擎、工具网站等，辅助工具如`Nmap` ，还有很多其他的工具。

###<font color=red>0x00 网站资源</font>
某些特定网站提供的功能能很好辅助我们完成信息收集的任务，例如`站长之家`，`whois` 等这些网站能为我们提供 whois 的相关信息，减少我们的时间成本，而且在线获取信息简单方便。

![网站资源](https://i.imgur.com/CAJGScZ.png)

| 分类 | 网站 |
|------|-----|
|whois| [who.is](https://who.is/) & [站长之家](http://whois.chinaz.com) |
|网站备案查询|[JSON在线](https://www.sojson.com)|
|DNS记录 | [https://who.is/dns](https://who.is/dns) |
|子域名| [http://i.links.cn/subdomain/](http://i.links.cn/subdomain/) |
|子域名|[http://searchdns.netcraft.com/](http://searchdns.netcraft.com/)|
|搜索引擎|[https://www.shodan.io/](https://www.shodan.io/)|
|指纹识别| [http://www.yunsee.cn/](http://www.yunsee.cn/)|
|端口扫描|[NMAP](https://hackertarget.com/ip-tools/)|
|网站安全扫描|[haoservice](http://haoservice.com/)|
|蜜罐检测|[shodan](https://www.shodan.io/)|
|链接检测|[API](https://hackertarget.com/ip-tools/)|
|IP定位|[haoservice](http://haoservice.com/) & [ipinfo](ipinfo.io)|
|路由跳点|[API](https://hackertarget.com/ip-tools/)|
|ping|[API](https://hackertarget.com/ip-tools/)|
|ip反向查找|[API](https://hackertarget.com/ip-tools/)|

##0x03代码编写
```
================================项目结构===================<br>
 >.
 >├── seekdog.py(主函数)  Main function<br>
 >├── plugins(功能函数目录)  Function function directory<br>
 >│   ├── APIscan.py(API函数文件) Store the API function<br>
 >│   ├── cmd_color_printers.py(windows彩色终端字体) Modify the color of the font output in the windows cmd<br>
 >│   ├── http_request.py(http请求) Two http request get methods and post methods<br>
 >│   ├── robots.py(读取rebots信息) Get rebots file information<br>
 >│   ├── nmap_port_info.py(辅助工具 Nmap (诸神之眼)) Need to install nmap locally and add it to environment variables<br>
 >│   ├── who_is.py(使用who.is和站长之家查询whois信息) Using third-party query target whois<br>
 >│   ├── output_html.py(将扫描结果的网页截取保存到本地)Save the scan result web page to local<br>
 >│   ├── cms_info.py(web指纹识别) Web fingerprinting<br>
 >│   ├── dns_info.py(DNS信息查询) DNS Lookup<br>
 >│   ├── subdomain.py(子域名查询) Cloudflare Detector<br>
 >├── config（配置文件） Profile<br>
 >│   ├── cms.txt(cms规则文件) Cms rule file<br>
 >│   └── config.py(参数配置) Parameter configuration<br>
 >├── output(输出目录) Output directory<br>
 >│   ├── whois1.html (whois信息) Whois information<br>
 >│   └── whois2.html (whois信息) Whois information<br>
 >│   └── rebots.txt (rebots.txt信息) Rebots.txt information<br>
 >│   ├── subdomain.xls (子域名信息) Subdomain information<br>
 >│   └── subdoamin.html (匹配域名) Match domain name<br>
 >│   └── nmap_info_result.txt (系统信息，端口信息等) System information, port information, etc.<br>
 >│   └── dns.html (dns信息) DNS information<br>
 >├── static(静态资源目录) Static resource directory<br>
 >├── requirements.txt(依赖库) Dependent library<br>
 >└── README.md(说明文档) Documentation<br>
=============================================================================================<br>
 ================plugin description================<br>
 ==========APIscan.py==============================<br>
 whois() : By api query whois information<br>
 beian() : Web site information<br>
 DNS class security<br>
     dnscl() : DNS Lookup + Cloudflare Detector<br>
     reverse_dns() : Reverse DNS resolution<br>
     zone() : Zone Transfer<br>
 webscan : Testing Website Security via API<br>
 webjson : Handle the json package file returned by the webscan() function and format the display<br>
 port() : Port Scan of nmap<br>
 header() : HTTP Header Grabber<br>
 honey(): Honeypot Detector<br>
 robots : Robots.txt Scanner<br>
 crawl() : Link Grabber<br>
 geo() : IP Location Finder<br>
 trace() : Traceroute<br>
 nping() : A ping test is used to determine the connectivity and latency of Internet connected hosts<br>
 reverse_ip() : Perform a reverse IP lookup to find all A records associated with an IP address<br>
 Social Engineering Tools<br>
     sphone() : Telephone inquiries<br>
     email() : Mailbox status detection<br>

```