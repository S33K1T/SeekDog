from django.shortcuts import render, HttpResponse

import json
from script.lib.console import core_class
from script.poc_exploit import poc_jc


# Create your views here.


def poc(request):
    coreclass = core_class()
    info = coreclass.do_version()
    poc_list = coreclass.do_list(0, 5)
    ctx = {}
    ctx['POC_version'] = info[0]
    ctx['CMS_num'] = info[1]
    ctx['POC_num'] = info[2]
    ctx['page'] = range(1, info[3]+1)
    ctx['poc_list'] = poc_list
    return render(request, "pages/poc/poc.html", ctx)


def ajax_POC(request):
    if (request.GET):
        coreclass = core_class()
        start = int(request.GET['start'])
        poc_list = coreclass.do_list(start, start + 5)
        return HttpResponse(json.dumps(poc_list))
    if (request.POST):
        type = request.POST['type']
        if (type == "search"):
            keywords = request.POST['keywords']
            coreclass = core_class()
            return HttpResponse(json.dumps(coreclass.do_search(keywords)))
        else:
            url = request.POST['url']
            poc_name = request.POST['poc_name']
            result = poc_jc(poc_name, url)
            return HttpResponse(json.dumps(result))
