from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from FuzzTools import CustomFuzz,PayloadOperation,SimpleFuzz
# Create your views here.

# 获取基础模糊测试页面
def GetBaseFuzzyPage(request):
    pass


# 基础模糊测试测试功能
def BaseFuzzy(request):
    pass

# 获取自定义模糊测试页面
def GetCustomFuzzPage(request):
    pass

# 获取替换文本
def GetReplaceText(request):
    pass

# 自定义模糊测试
def CustomFuzz(request):
    pass

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
