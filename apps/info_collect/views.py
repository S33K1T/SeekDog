from django.shortcuts import render, HttpResponse

import urllib.request
import json
from script.plugins.who_is import get_who_is_page
from script.plugins.portseek import run, txt2json
from script.plugins.cmsscan import cmsscan
from script.plugins.robots import get_rebots_info
from script.plugins.APIscan import crawl
# Create your views here.


def home_page(request):
    return render(request, "index.html")


def info_collect(request):
    return render(request, "pages/info/collection.html")


def ajax_whois(request):
    if request.POST:
        url = request.POST['url']
        get_who_is_page(url)
    return HttpResponse("ok")


def output_whois(request):
    return render(request, "output/whois2.html")


def ajax_DnsInfo(request):
    if (request.POST):
        url = request.POST['url']
        redns = "http://api.hackertarget.com/dnslookup/?q=" + url
        pns = urllib.request.urlopen(redns).read().decode('utf-8')
        return HttpResponse(pns)


def ajax_portScan(request):
    if (request.POST):
        urls = request.POST['url']
        url_list = urls.strip('\r\n').split('\r\n')
        run(url_list)
        result = txt2json()
    return HttpResponse(result)


def ajax_webFinger(request):
    if (request.POST):
        url = request.POST['url']
        cms_info = cmsscan(url)
        return HttpResponse(json.dumps(cms_info))


def ajax_robots(request):
    if request.POST:
        url = request.POST['url']
        result = get_rebots_info(url)
    return HttpResponse(result)


def ajax_linkCheck(request):
    if (request.POST):
        url = request.POST['url']
        domain = crawl(url)
        pcrawl = urllib.request.urlopen(domain).read().decode('utf-8')
        return HttpResponse(pcrawl)


def ajax_routerPop(request):
    if (request.POST):
        url = request.POST['url']
        domain = "https://api.hackertarget.com/mtr/?q=" + url
        ptrace = urllib.request.urlopen(domain).read().decode('utf-8')
        return HttpResponse(ptrace)


def ajax_ipLookup(request):
    if (request.POST):
        url = request.POST['url']
        domain = "https://api.hackertarget.com/reverseiplookup/?q=" + url
        freverseip = urllib.request.urlopen(domain).read().decode('utf-8')
        return HttpResponse(freverseip)
