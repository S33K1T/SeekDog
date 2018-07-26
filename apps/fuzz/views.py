from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from FuzzTools.CustomFuzz import *
from FuzzTools.PayloadOperation import *
from FuzzTools.SimpleFuzz import *
import json
# Create your views here.

# 获取基础模糊测试页面
def GetBaseFuzzyPage(request):
    payloadlists = PayloadOperation.getPayloadLists()
    return render(request,'pages/fuzzy/baseFuzzy.html',{'lists':payloadlists})

# 基础模糊测试测试功能
def BaseFuzzy(request):
    TestUrl = request.POST['url']
    Payload = request.POST['payloadName'].split('|')[0]
    Lists=[]
    TestType=""
    if Payload == "None":
        Lists = CreatePayloadList()
        TestType = "SQL注入"
    else:
        temp = PayloadOperation.getPayload(Payload)
        Lists=temp['BODY']
        TestType=temp['TYPE']
    Payload_UrlList = CreateFuzzUrlList(TestUrl,Lists)
    result = SimpleFuzz(Payload_UrlList)
    for i in result:
        i['payload'] = i['payload'].replace('<','&lt;').replace('>','&gt;').replace(' ','&nbsp;')
    return HttpResponse(json.dumps(result))

# 获取自定义模糊测试页面
def GetCustomFuzzPage(request):
    payloadlists = PayloadOperation.getPayloadLists()
    return render(request,'pages/fuzzy/userDefined.html',{'list':payloadlists})

# 获取替换文本
def GetReplaceText(request):
    url = "http://" + request.POST['url']
    method = request.POST['method']
    try:
        headers = json.loads("{" + request.POST['header'] + "}")
    except Exception as e:
        headers = None
    try:
        data = json.loads("{" + request.POST['data'] + "}")
    except Exception as e:
        data = None
        print("{" + request.POST['data'] + "}")
        print(e)
    cookies = request.POST['cookies']
    result = CreateDataPackge(url=url, method=method, header=headers, data=data, cookie=cookies)
    return HttpResponse(json.dumps(result))

# 自定义模糊测试
def CustomFuzz(request):
    print(request.POST)
    TestType = ""
    strategy = request.POST['strategy']
    request_data = request.POST['json_data']
    temp = FuzzTest(TestType,strategy,request_data)

    print(temp)
    return render(request,'pages/fuzzy/customReault.html',temp)
# 获取payload文件配置页面
def GetPayloadUpdatePage(request):
    payloadlists = getPayloadLists()
    return render(request,'pages/fuzzy/payloadEdit.html',{'lists':payloadlists})

# Payload文件配置功能
def PayloadUpdate(request):
    name = request.POST['PayloadName']
    PayloadType = request.POST['PayloadType']
    body = request.POST['PayloadBody']
    try:
        UpdatePayload(name,body,PayloadType)
    except Exception as e:
        return HttpResponse(e)
    return HttpResponseRedirect('fuzz/payloadUpdate/')
