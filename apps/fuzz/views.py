from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from FuzzTools import CustomFuzz,PayloadOperation,SimpleFuzz
import json
# Create your views here.

# 获取基础模糊测试页面
def GetBaseFuzzyPage(request):
    payloadlists = PayloadOperation.getPayloadLists()
    return render(request,'pages/fuzzy/baseFuzzy.html',{'lists':payloadlists})

# 基础模糊测试测试功能
def BaseFuzzy(request):
    TestUrl = request.POST['url']
    Payload = request.POST['payloadName']
    Lists=[]
    TestType=""
    if Payload == "None":
        Lists = SimpleFuzz.CreatePayloadList()
        TestType = "SQL注入"
    else:
        temp = PayloadOperation.getPayload(Payload)
        Lists=temp['BODY']
        TestType=temp['TYPE']
    Payload_UrlList = SimpleFuzz.CreateFuzzUrlList(TestUrl,Lists)
    result = SimpleFuzz.SimpleFuzz(Payload_UrlList)
    return HttpResponse(result)

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
        print(request.POST['data'])
        print(("{" + request.POST['data'] + "}")[10])
        print(e)
    cookies = request.POST['cookies']
    result = CustomFuzz.CreateDataPackge(url=url, method=method, header=headers, data=data, cookie=cookies)
    return HttpResponse(json.dumps(result))

# 自定义模糊测试
def CustomFuzz(request):
    pass
    TestType = request.POST['testType']
    strategy = request.POST['strategy']
    request_data = request.POST['json_data']
    temp = CustomFuzz.FuzzTest(TestType,strategy,request_data)
    return render(request,'pages/fuzzy/customReault.html',{'lists',temp})
# 获取payload文件配置页面
def GetPayloadUpdatePage(request):
    payloadlists = PayloadOperation.getPayloadLists()
    return render(request,'pages/fuzzy/payloadEdit.html',{'lists':payloadlists})

# Payload文件配置功能
def PayloadUpdate(request):
    name = request.POST['PayloadName']
    PayloadType = request.POST['PayloadType']
    body = request.POST['PayloadBody']
    try:
        PayloadOperation.UpdatePayload(name,body,PayloadType)
    except Exception as e:
        return HttpResponse(e)
    return HttpResponseRedirect('fuzz/payloadUpdate/')
